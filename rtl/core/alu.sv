module alu #(
    parameter XLEN = 32
) (
    input           [XLEN-1:0]  alu_in1_i,
    input           [XLEN-1:0]  alu_in2_i,
    input           [4:0]       alu_ctrl_i,
    output  logic   [XLEN-1:0]  alu_result_o,
    output  logic               alu_zero_o
);

    // ALU controls
    localparam ALU_ADD = 5'b0_0000;
    localparam ALU_AND = 5'b0_0001;
    localparam ALU_OR = 5'b0_0010;
    localparam ALU_XOR = 5'b0_0011;
    localparam ALU_SLL = 5'b0_0100;
    localparam ALU_SRL = 5'b0_0101;
    localparam ALU_SRA = 5'b0_0110;
    localparam ALU_SUB = 5'b1_0000;
    localparam ALU_SLTU = 5'b1_1000;
    localparam ALU_SLT = 5'b1_0111;

    always_comb begin
        case (alu_ctrl_i)
            ALU_ADD: begin
                alu_result_o = alu_in1_i + alu_in2_i;
            end
            ALU_AND: begin
                alu_result_o = alu_in1_i & alu_in2_i;
            end
            ALU_OR: begin
                alu_result_o = alu_in1_i | alu_in2_i;
            end
            ALU_XOR: begin
                alu_result_o = alu_in1_i ^ alu_in2_i;
            end
            ALU_SLL: begin
                alu_result_o = alu_in1_i << alu_in2_i;
            end
            ALU_SRL: begin
                alu_result_o = alu_in1_i >> alu_in2_i;
            end
            ALU_SRA: begin
                alu_result_o = $signed(alu_in1_i) >>> alu_in2_i;
            end
            ALU_SUB: begin
                alu_result_o = alu_in1_i - alu_in2_i;
            end
            ALU_SLTU: begin
                alu_result_o = (alu_in1_i < alu_in2_i) ? 1'b1 : 1'b0;
            end
            ALU_SLT: begin
                alu_result_o = ($signed(alu_in1_i) < $signed(alu_in2_i)) ? 1'b1 : 1'b0;
            end 
            default: begin
                alu_result_o = alu_in1_i + alu_in2_i;       // default operation
            end
        endcase
    end

    assign alu_zero_o = (alu_result_o == 32'b0) ? 1'b1 : 1'b0;

endmodule