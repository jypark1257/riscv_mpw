// `include "../RTL/headers/opcode.svh"

module branch_unit #(
    parameter XLEN = 32
) (
    input           [6:0]       opcode_i,
    input           [2:0]       funct3_i,
    input                       alu_zero_i,
    input           [XLEN-1:0]  pc_i,
    input           [31:0]      rs1_dout_i,
    input           [31:0]      imm_i,
    output  logic               branch_taken_o,
    output  logic   [XLEN-1:0]  pc_branch_o
);


    always_comb begin
        branch_taken_o = '0;
        pc_branch_o = '0;

        case (opcode_i)
            `OPCODE_JAL: begin
                branch_taken_o = 1'b1;
                pc_branch_o = pc_i + imm_i;
            end
            `OPCODE_JALR: begin
                if (funct3_i == 3'h0) begin
                    branch_taken_o = 1'b1;
                    pc_branch_o = rs1_dout_i + imm_i;
                end else begin
                    branch_taken_o = 1'b0;
                    // invalid branch pc
                end
            end
            `OPCODE_BRANCH: begin
                pc_branch_o = pc_i + imm_i;
                case (funct3_i)
                    `BRANCH_BEQ: begin
                        branch_taken_o = (alu_zero_i) ? 1'b1 : 1'b0;
                    end
                    `BRANCH_BNE: begin
                        branch_taken_o = (!alu_zero_i) ? 1'b1 : 1'b0;
                    end
                    `BRANCH_BLT: begin
                        branch_taken_o = (!alu_zero_i) ? 1'b1 : 1'b0;
                    end
                    `BRANCH_BGE: begin
                        branch_taken_o = (alu_zero_i) ? 1'b1 : 1'b0;
                    end
                    `BRANCH_BLTU: begin
                        branch_taken_o = (!alu_zero_i) ? 1'b1 : 1'b0;
                    end
                    `BRANCH_BGEU: begin
                        branch_taken_o = (alu_zero_i) ? 1'b1 : 1'b0;
                    end 
                    default: begin
                        branch_taken_o = 1'b0;
                    end
                endcase
            end 
            default: begin
                branch_taken_o = 1'b0;
            end
        endcase
    end

endmodule
