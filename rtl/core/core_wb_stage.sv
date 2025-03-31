
module core_wb_stage #(
    parameter XLEN = 32,
    parameter FLEN = 32
) (
    input           [3:0]       d_size_i,
    input                       d_unsigned_i,
    input           [2:0]       mem_to_reg_i,
    input           [XLEN-1:0]  data_rd_data_i,
    input           [XLEN-1:0]  imm_i,
    input           [XLEN-1:0]  pc_plus_4_i,
    input           [XLEN-1:0]  alu_result_i,
    input           [XLEN-1:0]  mul_result_i,       //M extension
    output  logic   [XLEN-1:0]  rd_din_o
);
    // REGISTER SOURCE
    localparam SRC_ALU = 3'b000;
    localparam SRC_DMEM = 3'b001;
    localparam SRC_PC_PLUS_4 = 3'b010;
    localparam SRC_IMM = 3'b011;
    localparam SRC_MUL = 3'b101;        // data form multiplier

    logic [31:0] dmem_dout;
    logic [31:0] dmem_dout_sized;
    logic [31:0] dmem_dout_byte;
    logic [31:0] dmem_dout_half;

    assign dmem_dout = data_rd_data_i;
    
    always @(*) begin
        dmem_dout_byte = '0;
        dmem_dout_half = '0;
        case (alu_result_i[1:0])
            2'b01: begin 
                dmem_dout_byte = {24'b0, dmem_dout[15:8]};
                dmem_dout_half = {16'b0, dmem_dout[23:8]};
            end
            2'b10: begin
                dmem_dout_byte = {24'b0, dmem_dout[23:16]};
                dmem_dout_half = {16'b0, dmem_dout[31:16]};
            end
            2'b11: begin
                dmem_dout_byte = {24'b0, dmem_dout[31:24]};
                //default (with strict-align, will not happen set default)
                dmem_dout_half = {16'b0, dmem_dout[15:0]};
            end
            default: begin
                dmem_dout_byte = {24'b0, dmem_dout[7:0]};
                dmem_dout_half = {16'b0, dmem_dout[15:0]};
            end
        endcase
    end


    always @(*) begin
        case (d_size_i)
            4'b0001: begin    // BYTE
                if (d_unsigned_i) begin
                    dmem_dout_sized = dmem_dout_byte;
                end else begin
                    dmem_dout_sized = $signed(dmem_dout_byte << 24) >>> 24;
                end
            end
            4'b0011: begin    // HALF WORD
                if (d_unsigned_i) begin
                    dmem_dout_sized = dmem_dout_half;
                end else begin
                    dmem_dout_sized = $signed(dmem_dout_half << 16) >>> 16;
                end
            end
            4'b1111: begin    // WORD
                dmem_dout_sized = dmem_dout;
            end
            default: begin
                dmem_dout_sized = dmem_dout;
            end
        endcase
    
    end

    always @(*) begin
        case(mem_to_reg_i)
            SRC_ALU:
                rd_din_o = alu_result_i;    // alu result
            SRC_DMEM:
                rd_din_o = dmem_dout_sized; // memory read
            SRC_PC_PLUS_4: 
                rd_din_o = pc_plus_4_i;     // pc + 4
            SRC_IMM:
                rd_din_o = imm_i;           // immediate
            SRC_MUL:
                rd_din_o = mul_result_i;    // M extension
            default: 
                rd_din_o = alu_result_i;
        endcase 
    end

endmodule