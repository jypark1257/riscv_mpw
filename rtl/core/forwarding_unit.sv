// `include "../RTL/headers/opcode.svh"

module forwarding_unit (
    input           [6:0]   opcode_i,
    input           [4:0]   rs1_i,
    input           [4:0]   rs2_i,
    input                   wb_reg_write_i,
    input           [4:0]   wb_rd_i,
    output  logic   [1:0]   forward_a_o,
    output  logic   [1:0]   forward_b_o
);

    localparam RF_DATA = 2'b01;
    localparam WB_DATA = 2'b10;

    always_comb begin
        forward_a_o = RF_DATA;
        if ((opcode_i != `OPCODE_JAL) && (opcode_i != `OPCODE_LUI) && (opcode_i != `OPCODE_AUIPC)) begin
            if (wb_reg_write_i && (wb_rd_i == rs1_i)) begin
                forward_a_o = WB_DATA;
            end else begin
                forward_a_o = RF_DATA;
            end
        end else begin
            forward_a_o = RF_DATA;
        end
    end

    always_comb begin
        forward_b_o = RF_DATA;
        if ((opcode_i == `OPCODE_R) || (opcode_i == `OPCODE_STORE) || (opcode_i == `OPCODE_BRANCH) || (opcode_i == `OPCODE_PIM)) begin
            if (wb_reg_write_i && (wb_rd_i == rs2_i)) begin
                forward_b_o = WB_DATA;
            end else begin
                forward_b_o = RF_DATA;
            end
        end else begin
            forward_b_o = RF_DATA;
        end
    end


endmodule
