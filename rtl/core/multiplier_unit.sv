module multiplier_unit #(
    parameter XLEN = 32
) (
    input           [XLEN-1:0]  mult_in1_i,
    input           [XLEN-1:0]  mult_in2_i,
    input           [6:0]       opcode_i,
    input           [6:0]       funct7_i,
    input           [2:0]       funct3_i,
    output  logic   [XLEN-1:0]  result_o,
    output  logic               muldiv_o    //multiply extention 인지 아닌지
);

    // OPCODES
    localparam OPCODE_R = 7'b0110011;

    // FUNCT7
    localparam FUNCT7_MULDIV = 7'b0000001;

    // FUNCT3
    localparam FUNCT3_MUL = 3'b000;
    localparam FUNCT3_MULH = 3'b001;
    localparam FUNCT3_MULHSU = 3'b010;
    localparam FUNCT3_MULHU = 3'b011;
    localparam FUNCT3_DIV = 3'b100;
    localparam FUNCT3_DIVU= 3'b101;
    localparam FUNCT3_REM = 3'b110;
    localparam FUNCT3_REMU = 3'b111;

    logic [XLEN+XLEN-1:0] mult_result_signed;
    logic [XLEN+XLEN-1:0] mult_result_unsigned;
    logic [XLEN+XLEN-1:0] mult_result_signed_unsigned;
    logic [XLEN+XLEN-1:0] tc_mult_result_signed_unsigned;
    logic [XLEN-1:0] tc_mult_in1;

    assign tc_mult_in1 = ~mult_in1_i + 1'b1;
    assign tc_mult_result_signed_unsigned = ~mult_result_signed_unsigned + 1'b1;

    DW02_mult #(
        .A_width        (XLEN),
        .B_width        (XLEN)
    ) mult_signed (
        .A              (mult_in1_i),
        .B              (mult_in2_i),
        .TC             (1'b1),
        .PRODUCT        (mult_result_signed)
    );

    DW02_mult #(
        .A_width        (XLEN),
        .B_width        (XLEN)
    ) mult_unsigned (
        .A              (mult_in1_i),
        .B              (mult_in2_i),
        .TC             (1'b0),
        .PRODUCT        (mult_result_unsigned)
    );

    DW02_mult #(
        .A_width        (XLEN),
        .B_width        (XLEN)
    ) mult_signed_unsigned (
        .A              (tc_mult_in1),
        .B              (mult_in2_i),
        .TC             (1'b0),
        .PRODUCT        (mult_result_signed_unsigned)
    );

    logic [XLEN-1:0] div_result_signed;
    logic [XLEN-1:0] div_result_unsigned;
    logic [XLEN-1:0] rem_result_signed;
    logic [XLEN-1:0] rem_result_unsigned;

    divv #(
        .a_width        (XLEN),
        .b_width        (XLEN)
    ) div_signed (
        .a              (mult_in1_i), 
        .b              (mult_in2_i), 
        .quotient       (div_result_signed), 
        .remainder      (rem_result_signed)
    );

    DW_div #(
        .a_width        (XLEN),
        .b_width        (XLEN),
        .tc_mode        (1'b0),
        .rem_mode       (1'b1)
    ) div_unsigned (
        .a              (mult_in1_i), 
        .b              (mult_in2_i), 
        .quotient       (div_result_unsigned), 
        .remainder      (rem_result_unsigned), 
        .divide_by_0    ()
    );

    //always_comb begin
    always @(*) begin
        if ((opcode_i == OPCODE_R) && (funct7_i == FUNCT7_MULDIV)) begin         
            muldiv_o = 1'b1;

            case (funct3_i) 
                FUNCT3_MUL: begin
                    result_o = mult_result_signed[XLEN-1:0];
                end 
                FUNCT3_MULH: begin
                    result_o = mult_result_signed[XLEN+XLEN-1:XLEN];
                end    
                FUNCT3_MULHSU: begin
                    if (mult_in1_i[XLEN-1]) begin
                        result_o = tc_mult_result_signed_unsigned[XLEN+XLEN-1:XLEN];
                    end else begin 
                        result_o = mult_result_unsigned[XLEN+XLEN-1:XLEN];
                    end
                end        
                FUNCT3_MULHU: begin
                    result_o = mult_result_unsigned[XLEN+XLEN-1:XLEN];
                end
                FUNCT3_DIV: begin
                    result_o = div_result_signed;
                end
                FUNCT3_DIVU: begin
                    result_o = div_result_unsigned;
                end
                FUNCT3_REM: begin
                    result_o = rem_result_signed;
                end
                FUNCT3_REMU: begin
                    result_o = rem_result_unsigned;
                end            
            endcase           
        end else begin
            result_o = 32'b0;
            muldiv_o = 1'b0;
        end
    end

endmodule



