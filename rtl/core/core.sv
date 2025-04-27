`ifndef COCOTB
    `include "../headers/opcode.svh"
    `include "../headers/pipe_reg.svh"
`endif 
module core #(
    parameter bit FPGA = 0,
    parameter XLEN = 32,
    parameter FLEN = 32,
    parameter RESET_PC = 32'h1000_0000

) (
    input                       clk_i,
    input                       rst_ni,
    // instruction interface
    output  logic   [XLEN-1:0]  instr_addr_o,
    input           [XLEN-1:0]  instr_rd_data_i,
    output  logic   [XLEN-1:0]  instr_wr_data_o,
    output  logic   [3:0]       instr_size_o,
    output  logic               instr_read_o,
    output  logic               instr_write_o,
    // data interface
    output  logic               req_dmem_o,
    input                       gnt_dmem_i,
    output  logic   [XLEN-1:0]  data_addr_o,
    input           [XLEN-1:0]  data_rd_data_i,
    output  logic   [XLEN-1:0]  data_wr_data_o,
    output  logic   [3:0]       data_size_o,
    output  logic               data_read_o,
    output  logic               data_write_o,
    // DMA status
    input                       dma_busy_i,
    // DMA interface
    output  logic               dma_en_o,
    output  logic   [2:0]       dma_funct3_o,
    output  logic   [3:0]       dma_sel_pim_o,  
    output  logic   [12:0]      dma_size_o,
    output  logic   [31:0]      dma_mem_addr_o

);

    // pipline registers
    pipe_if_id      id;
    pipe_id_ex      ex;
    pipe_ex_wb      wb;

    logic pc_write;
    logic [XLEN-1:0] pc_curr;
    logic [XLEN-1:0] pc_instr;

    logic branch_taken;
    logic [XLEN-1:0] pc_branch;
    
    logic [6:0] opcode;
    logic [4:0] rd;
    logic [2:0] funct3;
    logic [4:0] rs1;
    logic [4:0] rs2;
    logic [6:0] funct7;

    // DMA control signals
    logic dma_en;

    logic mem_read;
    logic mem_write;
    logic reg_write;
    logic [2:0] mem_to_reg;
    logic [3:0] d_size;
    logic d_unsigned;
    logic muldiv_en;

    logic [XLEN-1:0] wr_data;
    logic [XLEN-1:0] forward_in1;
    logic [XLEN-1:0] forward_in2;
    logic [XLEN-1:0] alu_result;
    logic ex_mem_write;
    logic ex_valid;
    logic ex_valid_pc;

    logic [XLEN-1:0] imm;

    logic [XLEN-1:0] rs1_dout;
    logic [XLEN-1:0] rs2_dout;

    logic [XLEN-1:0] rd_din;

    logic dma_stall;
    logic ex_stall;
    logic if_flush;    
    logic id_flush;
    logic if_stall;
    logic id_stall;

    logic [XLEN-1:0] mul_result;        // M extension

    // --------------------------------------------------------

    core_if_stage #(
        .XLEN(32),
        .RESET_PC(RESET_PC)
    ) core_IF (
        .clk_i              (clk_i),
        .rst_ni             (rst_ni),
        .pc_write_i         (pc_write),
        .branch_taken_i     (branch_taken),
        .pc_branch_i        (pc_branch),
        .pc_curr_o          (pc_curr),
        .pc_instr_o         (pc_instr)
    );

    logic valid_q;
    logic valid_d;
    logic invalid_instr_flush;

    // Instruction memory
    logic [XLEN-1:0] instr;
    logic [XLEN-1:0] instr_compressed;
    logic is_compressed;
    logic is_next_instr_compressed;
    assign pc_write = ((!dma_stall) && (!ex_stall_pc) && (!muldiv_en)) ? 1'b1 : 1'b0;

    // instruction memory interface
    assign instr_addr_o = (branch_taken) ? pc_branch : pc_curr;
    assign instr = instr_rd_data_i;
    assign instr_wr_data_o = '0;
    assign instr_size_o = 4'b1111;        // always 32-bit access
    assign instr_read_o = ((!dma_stall) && (!ex_stall)) ? 1'b1 : 1'b0;
    assign instr_write_o = 1'b0;
    // determine compressed instruction
    assign is_compressed = (instr[1:0] != 2'b11);
    always_comb begin
        is_next_instr_compressed = '0;
        if (is_compressed) begin
            is_next_instr_compressed = (instr[17:16] != 2'b11);
        end else begin
            is_next_instr_compressed = '0;
        end
    end

    // valid register
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            valid_q <= 1'b1;
        end else begin
            if (branch_taken) begin
                valid_q <= 1'b1;
            end else begin
                valid_q <= valid_d;
            end
        end
    end
    
    // determine if the instruction has to be ignored
    always_comb begin
        valid_d = 1'b0;
        if (valid_q) begin  // 16b or 32l or init
            if (is_compressed) begin    // 16b  
                if (is_next_instr_compressed) begin // 16b, 16b
                    valid_d = 1'b1;
                end else begin  // 32l
                    valid_d = 1'b1;
                end
            end else begin  // 32l
                if (pc_curr == RESET_PC) begin // initial instruction
                    valid_d = 1'b1;
                end else begin
                    valid_d = 1'b0;
                end
            end
        end else begin  // 32h
            valid_d = 1'b1;
        end
    end

    assign invalid_instr_flush = (valid_q == 1'b0);

    // --------------------------------------------------------

    assign if_flush = (invalid_instr_flush || branch_taken) ? 1'b1 : 1'b0;
    assign if_stall = (dma_stall || ex_stall) ? 1'b1: 1'b0;

    // IF/ID pipeline register
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            id <= '0;
        end else begin
            if (if_flush) begin
                id <= '0;
            end else if (if_stall) begin
                id <= id;
            end else begin
                id.pc <= pc_instr;
                id.is_compressed <= is_compressed;
                id.instr <= instr; 
            end
        end
    end

    // --------------------------------------------------------

    core_id_stage #(
        .XLEN(32)
    ) core_ID (
        .clk_i              (clk_i),
        .rst_ni             (rst_ni),
        .is_compressed_i    (id.is_compressed),
        .instr_i            (id.instr),
        .rd_din_i           (rd_din),
        .wb_rd_i            (wb.rd),
        .wb_reg_write_i     (wb.reg_write),
        .opcode_o           (opcode),
        .rd_o               (rd),
        .funct3_o           (funct3),
        .rs1_o              (rs1),
        .rs2_o              (rs2),
        .funct7_o           (funct7),
        .imm_o              (imm),
        .mem_read_o         (mem_read),
        .mem_write_o        (mem_write),
        .reg_write_o        (reg_write),
        .mem_to_reg_o       (mem_to_reg),
        .d_size_o           (d_size),
        .d_unsigned_o       (d_unsigned),
        .dma_en_o           (dma_en),
        .rs1_dout_o         (rs1_dout),
        .rs2_dout_o         (rs2_dout),
        .muldiv_en_o        (muldiv_en)
    );


    // --------------------------------------------------------

    // request for dmem use
    assign req_dmem_o = ((mem_read || mem_write) && (dma_stall == 1'b0));
    

    // --------------------------------------------------------
    assign id_flush = (branch_taken || dma_stall) ? 1'b1 : 1'b0;
    assign id_stall = (ex_stall) ? 1'b1 : 1'b0;

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            ex <= '0;
        end else begin
            if (id_flush) begin
                ex <= '0;
            end else if (id_stall) begin
                ex <= ex;
            end else begin
                ex.pc <= id.pc;
                ex.is_compressed <= id.is_compressed;
                ex.opcode <= opcode;
                ex.rd <= rd;
                ex.funct3 <= funct3;
                ex.rs1 <= rs1;
                ex.rs2 <= rs2;
                ex.funct7 <= funct7;
                ex.imm <= imm;
                ex.mem_read <= mem_read;
                ex.mem_write <= mem_write;
                ex.reg_write <= reg_write;
                ex.mem_to_reg <= mem_to_reg;
                ex.d_size <= d_size;
                ex.d_unsigned <= d_unsigned;
                ex.dma_en <= dma_en;
                ex.rs1_dout <= rs1_dout;
                ex.rs2_dout <= rs2_dout;
            end
        end
    end

    // --------------------------------------------------------

    core_ex_stage #(
        .FPGA(FPGA),
        .XLEN(32)
    ) core_EX (
        .clk_i          (clk_i),
        .rst_ni         (rst_ni),
        .pc_i           (ex.pc),
        .opcode_i       (ex.opcode),
        .rd_i           (ex.rd),
        .funct3_i       (ex.funct3),
        .rs1_i          (ex.rs1),
        .rs2_i          (ex.rs2),
        .funct7_i       (ex.funct7),
        .rs1_dout_i     (ex.rs1_dout),
        .rs2_dout_i     (ex.rs2_dout),
        .imm_i          (ex.imm),
        .rd_din_i       (rd_din),
        .wb_rd_i        (wb.rd),
        .wb_reg_write_i (wb.reg_write),
        .alu_result_o   (alu_result),
        .branch_taken_o (branch_taken),
        .pc_branch_o    (pc_branch),
        .forward_in1_o  (forward_in1),
        .forward_in2_o  (forward_in2),
        .mul_result_o   (mul_result),        // M extension
        .ex_valid_o     (ex_valid),
        .ex_valid_pc_o  (ex_valid_pc)
    );

    assign dma_stall = (dma_busy_i || ex.dma_en) ? 1'b1 : 1'b0;

    assign ex_stall_pc = (!ex_valid_pc) ? 1'b1 : 1'b0;

    assign ex_stall = (!ex_valid) ? 1'b1 : 1'b0;


    // DMA interface
    assign dma_en_o = ex.dma_en;
    assign dma_funct3_o = ex.funct3;
    assign dma_sel_pim_o = ex.imm[3:0];
    assign dma_size_o = forward_in1[12:0];
    assign dma_mem_addr_o = forward_in2;
    

    // data interface set
    // un-aligned store
    always @(*) begin
        wr_data = '0;
        data_size_o = '0;
        case (alu_result[1:0])
            2'b01: begin    // 
                wr_data = forward_in2 << 8;
                data_size_o = ex.d_size << 1;
            end
            2'b10: begin    // 
                wr_data = forward_in2 << 16;
                data_size_o = ex.d_size << 2;
            end
            2'b11: begin    // 
                wr_data = forward_in2 << 24;
                data_size_o = ex.d_size << 3;
            end 
            default: begin    // 
                wr_data = forward_in2;
                data_size_o = ex.d_size;
            end
        endcase
    end
    assign data_addr_o = alu_result;
    assign data_wr_data_o = wr_data;
    assign data_read_o = ex.mem_read;
    assign data_write_o = ex.mem_write;

    // --------------------------------------------------------

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            wb <= '0;
        end else begin
            wb.pc_plus_4 <= (ex.is_compressed) ? (ex.pc + 2) : (ex.pc + 4);
            wb.rd <= ex.rd;
            wb.imm <= ex.imm;
            wb.alu_result <= alu_result;
            wb.mul_result <= mul_result;        // M extension
            wb.reg_write <= ex.reg_write;
            wb.mem_to_reg <= ex.mem_to_reg;
            wb.d_size <= ex.d_size;
            wb.d_unsigned <= ex.d_unsigned;
        end
    end

    // --------------------------------------------------------

    core_wb_stage #(
        .XLEN(32)
    ) core_WB_0 (
        .d_size_i       (wb.d_size),
        .d_unsigned_i   (wb.d_unsigned),
        .mem_to_reg_i   (wb.mem_to_reg),
        .data_rd_data_i (data_rd_data_i),
        .imm_i          (wb.imm),
        .pc_plus_4_i    (wb.pc_plus_4),
        .alu_result_i   (wb.alu_result),
        .mul_result_i   (wb.mul_result),        // M extension
        .rd_din_o       (rd_din)
    );

    // --------------------------------------------------------

endmodule
