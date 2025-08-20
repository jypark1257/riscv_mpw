`include "opcode.svh"

module immediate_generator (
    input           [6:0]   opcode_i,
    input           [4:0]   rd_i,
    input           [2:0]   fucnt3_i,
    input           [4:0]   rs1_i,
    input           [4:0]   rs2_i,
    input           [6:0]   funct7_i,
    output  logic   [31:0]  imm_o
);

    // SHIFTS
    localparam FUNCT3_SL = 3'b001;
    localparam FUNCT3_SR = 3'b101;

    logic [11:0] imm_i;     // immediate
    logic [11:0] imm_s;     // store
    logic [12:0] imm_b;     // branch
    logic [20:0] imm_j;     // jump
    logic [4:0]  sht_amt;   // shift amount
    logic [19:0] imm_u;     //upper immediate

    logic [31:0] imm_pim_sext;
    logic [31:0] imm_i_sext;
    logic [31:0] imm_s_sext;
    logic [31:0] imm_b_sext;
    logic [31:0] sht_amt_sext;
    logic [31:0] imm_j_sext;
    logic [31:0] imm_u_zfill;

    // Immediate parsing
    assign imm_i = {funct7_i, rs2_i};
    assign imm_s = {funct7_i, rd_i};
    assign imm_b = {funct7_i[6], rd_i[0], funct7_i[5:0], rd_i[4:1], 1'b0};
    assign imm_j = {funct7_i[6], rs1_i, fucnt3_i, rs2_i[0], funct7_i[5:0], rs2_i[4:1], 1'b0};
    assign sht_amt = rs2_i;
    assign imm_u = {funct7_i, rs2_i, rs1_i, fucnt3_i};
    

    // Extension
    assign imm_i_sext = {{20{imm_i[11]}}, imm_i};
    assign imm_s_sext = {{20{imm_s[11]}}, imm_s};
    assign imm_b_sext = {{19{imm_b[12]}}, imm_b};
    assign sht_amt_sext = {{27{1'b0}}, sht_amt};
    assign imm_j_sext = {{11{imm_j[20]}}, imm_j};
    assign imm_u_zfill = {imm_u, 12'b0};
    assign imm_pim_sext = imm_s_sext;

    always_comb begin
        imm_o = '0;

        case (opcode_i)
            `OPCODE_I: begin
                if ((fucnt3_i == FUNCT3_SL) || (fucnt3_i == FUNCT3_SR)) begin
                    imm_o = sht_amt_sext;
                end else begin
                    imm_o = imm_i_sext;
                end
            end
            `OPCODE_STORE: begin
                imm_o = imm_s_sext;
            end
            `OPCODE_LOAD: begin
                imm_o  = imm_i_sext;
            end 
            `OPCODE_BRANCH: begin
                imm_o = imm_b_sext;
            end
            `OPCODE_JALR: begin
                imm_o = imm_i_sext;         // later, PC = rs1 + imm_i_sext
            end 
            `OPCODE_JAL: begin
                imm_o = imm_j_sext;         // later, PC = PC + imm_i_sext
            end
            `OPCODE_AUIPC: begin
                imm_o = imm_u_zfill;        // later, rd = PC + imm_u_zfill
            end
            `OPCODE_LUI: begin
                imm_o = imm_u_zfill;
            end
            `OPCODE_PIM: begin
                imm_o = imm_pim_sext;
            end
            default: 
                imm_o = '0;
        endcase
    end

endmodule
