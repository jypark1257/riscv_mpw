`ifndef COCOTB
    `include "../rtl/headers/opcode.svh"
`endif 

module alu_ctrl_unit (
    input           [6:0]   opcode_i,
    input           [6:0]   funct7_i,
    input           [2:0]   funct3_i,
    output  logic   [4:0]   alu_ctrl_o
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
        if (opcode_i == `OPCODE_BRANCH) begin
            case (funct3_i)
                `BRANCH_BEQ: begin
                    alu_ctrl_o = ALU_SUB;
                end
                `BRANCH_BNE: begin
                    alu_ctrl_o = ALU_SUB;
                end
                `BRANCH_BLT: begin
                    alu_ctrl_o = ALU_SLT;
                end
                `BRANCH_BGE: begin
                    alu_ctrl_o = ALU_SLT;
                end
                `BRANCH_BLTU: begin
                    alu_ctrl_o = ALU_SLTU;
                end
                `BRANCH_BGEU: begin
                    alu_ctrl_o = ALU_SLTU;
                end
                default: begin
                    alu_ctrl_o = ALU_SUB;
                end
            endcase
        end else if ((opcode_i == `OPCODE_R) || (opcode_i == `OPCODE_I)) begin
            case (funct3_i)
                `FUNCT3_ADD_SUB: begin
                    if (opcode_i == `OPCODE_R) begin
                        if (funct7_i == 7'h20) begin            // `FUNCT3_SUB
                            alu_ctrl_o = ALU_SUB;
                        end else if (funct7_i == 7'h00) begin   // `FUNCT3_ADD
                            alu_ctrl_o = ALU_ADD;
                        end else begin
                            alu_ctrl_o = ALU_ADD;
                        end
                    end else begin
                        alu_ctrl_o = ALU_ADD;                // `OPCODE_I
                    end
                end
                `FUNCT3_SLL: begin
                    alu_ctrl_o = ALU_SLL;
                end
                `FUNCT3_SLT: begin
                    alu_ctrl_o = ALU_SLT;
                end
                `FUNCT3_SLTU: begin
                    alu_ctrl_o = ALU_SLTU;
                end
                `FUNCT3_XOR: begin
                    alu_ctrl_o = ALU_XOR;
                end
                `FUNCT3_SRL_SRA: begin
                    if (funct7_i == 7'h00) begin            // `FUNCT3_SRL
                        alu_ctrl_o = ALU_SRL;
                    end else if (funct7_i == 7'h20) begin   // `FUNCT3_SRA
                        alu_ctrl_o = ALU_SRA;
                    end else begin
                        alu_ctrl_o = ALU_ADD;
                    end
                end
                `FUNCT3_OR: begin
                    alu_ctrl_o = ALU_OR;
                end
                `FUNCT3_AND: begin
                    alu_ctrl_o = ALU_AND;
                end 
                //default: begin
                //    alu_ctrl_o = ALU_ADD;
				//end
            endcase
        end else begin
            alu_ctrl_o = ALU_ADD;                    // set default to ADD operation, for LOAD, STORE, JAL(R), and AUIPC
        end
    end

endmodule
