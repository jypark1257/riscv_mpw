
module core_id_stage #(
    parameter XLEN = 32
) (
    input                       clk_i,
    input                       rst_ni,
    input           [XLEN-1:0]  instr_i,
    input           [XLEN-1:0]  rd_din_i,
    input           [4:0]       wb_rd_i,
    input                       wb_reg_write_i,
    output  logic   [6:0]       opcode_o,
    output  logic   [4:0]       rd_o,
    output  logic   [2:0]       funct3_o,
    output  logic   [4:0]       rs1_o,
    output  logic   [4:0]       rs2_o,
    output  logic   [6:0]       funct7_o,
    output  logic               mem_read_o,
    output  logic               mem_write_o,
    output  logic               reg_write_o,
    output  logic   [2:0]       mem_to_reg_o,
    output  logic   [3:0]       d_size_o,
    output  logic               d_unsigned_o,
    output  logic               dma_en_o,
    output  logic   [XLEN-1:0]  imm_o,
    output  logic   [XLEN-1:0]  rs1_dout_o,
    output  logic   [XLEN-1:0]  rs2_dout_o
);

    // instruction parsing
    assign opcode_o = instr_i[6:0];
    assign rd_o = instr_i[11:7];
    assign funct3_o = instr_i[14:12];
    assign rs1_o = instr_i[19:15];
    assign rs2_o = instr_i[24:20];
    assign funct7_o = instr_i[31:25];
    
    // Main control unit
    decoder_unit dec_u (
        .opcode_i       (opcode_o),
        .rd_i           (rd_o),
        .fucnt3_i       (funct3_o),
        .rs1_i          (rs1_o),
        .funct7_i       (funct7_o),
        .reg_write_o    (reg_write_o),
        .d_size_o       (d_size_o),
        .d_unsigned_o   (d_unsigned_o),
        .mem_to_reg_o   (mem_to_reg_o),
        .mem_read_o     (mem_read_o),
        .mem_write_o    (mem_write_o),
        .dma_en_o       (dma_en_o)
    );

    // Immrdiate generator
    immediate_generator imm_gen (
        .opcode_i   (opcode_o),
        .rd_i       (rd_o),
        .fucnt3_i   (funct3_o),
        .rs1_i      (rs1_o),
        .rs2_i      (rs2_o),
        .funct7_i   (funct7_o),
        .imm_o      (imm_o)
    );
    
    register_file #(
        .XLEN           (XLEN)
    ) rf (
        .clk_i          (clk_i),
        .rst_ni         (rst_ni),
        .rs1_i          (rs1_o),
        .rs2_i          (rs2_o),
        .rd_i           (wb_rd_i),
        .rd_din_i       (rd_din_i),
        .reg_write_i    (wb_reg_write_i),
        .rs1_dout_o     (rs1_dout_o),
        .rs2_dout_o     (rs2_dout_o)
    );

endmodule