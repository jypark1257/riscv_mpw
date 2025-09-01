`include "opcode.svh"

module core_ex_stage #(
    parameter bit FPGA = 0,
    parameter XLEN = 32
) (
    input                       clk_i,
    input                       rst_ni,
    input           [XLEN-1:0]  pc_i,
    input           [6:0]       opcode_i,
    input           [4:0]       rd_i,
    input           [2:0]       funct3_i,
    input           [4:0]       rs1_i,
    input           [4:0]       rs2_i,
    input           [6:0]       funct7_i,
    input           [XLEN-1:0]  rs1_dout_i,
    input           [XLEN-1:0]  rs2_dout_i,
    input           [XLEN-1:0]  imm_i,
    input           [XLEN-1:0]  rd_din_i,
    input           [4:0]       wb_rd_i,
    input                       wb_reg_write_i,
    output  logic   [XLEN-1:0]  alu_result_o,
    output  logic               branch_taken_o,
    output  logic   [XLEN-1:0]  pc_branch_o,
    output  logic   [XLEN-1:0]  forward_in1_o,
    output  logic   [XLEN-1:0]  forward_in2_o,
    output  logic   [XLEN-1:0]  mul_result_o
);

    logic [1:0] forward_a;
    logic [1:0] forward_b;

    logic [4:0] alu_control;
    logic       alu_zero;

    logic is_muldiv;

    // ALU control unit
    alu_ctrl_unit alu_ctrl_u (
        .opcode_i       (opcode_i),
        .funct7_i       (funct7_i),
        .funct3_i       (funct3_i),
        .alu_ctrl_o     (alu_control)
    );

    // Forwarding unit
    forwarding_unit f_u (
        .opcode_i           (opcode_i),
        .rs1_i              (rs1_i),
        .rs2_i              (rs2_i),
        .wb_reg_write_i     (wb_reg_write_i),
        .wb_rd_i            (wb_rd_i),
        .forward_a_o        (forward_a),
        .forward_b_o        (forward_b)
    );

    // forward rs1
    // always_comb
    always @(*) begin
        if (forward_a == 2'b10) begin   // WB STAGE
            forward_in1_o = rd_din_i;
        end else begin
            if (opcode_i == `OPCODE_AUIPC) begin
                forward_in1_o = pc_i;
            end else begin
                forward_in1_o = rs1_dout_i;
            end
        end
    end

    // forward rs2
    always @(*) begin
        if (forward_b == 2'b10) begin   // WB STAGE
            forward_in2_o = rd_din_i;
        end else begin
            if ((opcode_i == `OPCODE_R) || (opcode_i == `OPCODE_STORE) || (opcode_i == `OPCODE_BRANCH) || (opcode_i == `OPCODE_PIM)) begin
                forward_in2_o = rs2_dout_i;
            end else begin
                forward_in2_o = imm_i;
            end
        end
    end

    logic [31:0] alu_in2;

    always @(*) begin
        if (opcode_i == `OPCODE_STORE) begin
            alu_in2 = imm_i;
        end else if (opcode_i == `OPCODE_R) begin
            if ((funct3_i == 3'h1) || (funct3_i == 3'h5)) begin
                alu_in2 = {27'b0, forward_in2_o[4:0]};
            end else begin
                alu_in2 = forward_in2_o;
            end
        end else begin
            alu_in2 = forward_in2_o;
        end
    end

    // assign alu_in2 = (opcode_i == `OPCODE_STORE) ? imm_i : forward_in2_o;

    // Arithmetic logic unit
    alu #(
        .XLEN           (XLEN)
    ) alu (
        .alu_in1_i      (forward_in1_o),
        .alu_in2_i      (alu_in2),
        .alu_ctrl_i     (alu_control),
        .alu_result_o   (alu_result_o),
        .alu_zero_o     (alu_zero)
    );

    // Branch unit
    branch_unit #(
        .XLEN           (XLEN)
    ) b_u (
        .opcode_i       (opcode_i),
        .funct3_i       (funct3_i),
        .alu_zero_i     (alu_zero),
        .pc_i           (pc_i),
        .rs1_dout_i     (forward_in1_o),
        .imm_i          (imm_i),
        .branch_taken_o (branch_taken_o),
        .pc_branch_o    (pc_branch_o)
    );

    // Multiplier and Divider
    muldiv_unit #(
        .FPGA(1),
        .XLEN(XLEN)
    ) m_u (
        .clk_i(clk_i),
        .rst_ni(rst_ni),
        .mult_in1_i(forward_in1_o),
        .mult_in2_i(forward_in2_o),
        .opcode_i(opcode_i),
        .funct7_i(funct7_i),
        .funct3_i(funct3_i),
        .result_o(mul_result_o),
        .is_muldiv_o(is_muldiv)
    ); 


endmodule
