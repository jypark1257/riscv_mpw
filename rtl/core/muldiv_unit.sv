//`include "../headers/opcode.svh"

module muldiv_unit #(
    parameter XLEN = 32,
    parameter NUM_STAGE= 2
) (
    input                       clk_i,
    input                       rst_ni,
    input           [XLEN-1:0]  mult_in1_i,
    input           [XLEN-1:0]  mult_in2_i,
    input           [6:0]       opcode_i,
    input           [6:0]       funct7_i,
    input           [2:0]       funct3_i,
    output  logic   [XLEN-1:0]  result_o,
    output  logic               is_muldiv_o,
    output  logic               valid_o
);

    // FUNCT3
    // localparam FUNCT3_MUL = 3'b000;
    // localparam FUNCT3_MULH = 3'b001;
    // localparam FUNCT3_MULHSU = 3'b010;
    // localparam FUNCT3_MULHU = 3'b011;
    // localparam FUNCT3_DIV = 3'b100;
    // localparam FUNCT3_DIVU = 3'b101;
    // localparam FUNCT3_REM = 3'b110;
    // localparam FUNCT3_REMU = 3'b111;

    localparam NUM_PIPES = NUM_STAGE - 1;

    logic is_muldiv;


    logic [XLEN-1:0] mult_in1_q[NUM_PIPES];
    logic signed_overflow[NUM_PIPES];
    logic divide_by_0[NUM_PIPES];
    logic [2:0] funct3_q[NUM_PIPES];
    logic [NUM_PIPES-1:0] valid_counter;
    
    logic [XLEN-1:0] mult_in1_unsigned;
    logic sign_mult_in1[NUM_PIPES];
    logic [(XLEN+1)-1:0] md_op1;
    logic [(XLEN+1)-1:0] md_op2;
    logic [(XLEN+1)+(XLEN+1)-1:0] mult_result;
    logic [(XLEN+1)+(XLEN+1)-1:0] mult_result_signed_unsigned;

    logic [(XLEN+1)-1:0] div_result;
    logic [(XLEN+1)-1:0] rem_result;
    

    // muldiv decoder
    always_comb begin
        is_muldiv = '0;
        if ((opcode_i == `OPCODE_R) && (funct7_i == `FUNCT7_MULDIV)) begin         
            is_muldiv = 1'b1;
        end else begin
            is_muldiv = '0;
        end
    end
    assign is_muldiv_o = is_muldiv;

    // operand decoder
    always @(*) begin
        md_op1 = {1'b0, mult_in1_i};
        md_op2 = {1'b0, mult_in2_i};
        mult_in1_unsigned = ~mult_in1_i + 1'b1;
        case (funct3_i)
            `FUNCT3_MUL, `FUNCT3_MULH: begin
                md_op1 = {mult_in1_i[XLEN-1], mult_in1_i};
                md_op2 = {mult_in2_i[XLEN-1], mult_in2_i};
            end 
            `FUNCT3_MULHSU: begin
                if (mult_in1_i[XLEN-1]) begin
                    md_op1 = {1'b0, mult_in1_unsigned};
                end else begin
                    md_op1 = {1'b0, mult_in1_i};
                end
                md_op2 = {1'b0, mult_in2_i};
            end
            `FUNCT3_MULHU: begin
                md_op1 = {1'b0, mult_in1_i};
                md_op2 = {1'b0, mult_in2_i};
            end
            `FUNCT3_DIV: begin
                md_op1 = {mult_in1_i[XLEN-1], mult_in1_i};
                md_op2 = {mult_in2_i[XLEN-1], mult_in2_i};
            end
            `FUNCT3_DIVU: begin
                md_op1 = {1'b0, mult_in1_i};
                md_op2 = {1'b0, mult_in2_i};
            end
            `FUNCT3_REM: begin
                md_op1 = {mult_in1_i[XLEN-1], mult_in1_i};
                md_op2 = {mult_in2_i[XLEN-1], mult_in2_i};
            end
            `FUNCT3_REMU: begin
                md_op1 = {1'b0, mult_in1_i};
                md_op2 = {1'b0, mult_in2_i};
            end
            default: begin
                md_op1 = {1'b0, mult_in1_i};
                md_op2 = {1'b0, mult_in2_i};
            end
        endcase
    end

    // pipe funct3 and sign op1
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            for (int i = 0; i < NUM_PIPES; ++i) begin
                signed_overflow[i] <= '0;
                divide_by_0[i] <= '0;
                sign_mult_in1[i] <= '0;
                funct3_q[i] <= '0;
            end
        end else begin
            mult_in1_q[0] <= mult_in1_i;
            signed_overflow[0] <= ((mult_in1_i == 32'h80000000) && (mult_in2_i == 32'hFFFFFFFF));
            divide_by_0[0] <= (mult_in2_i == 32'b0);
            sign_mult_in1[0] <= mult_in1_i[XLEN-1];
            funct3_q[0] <= funct3_i;
            for (int i = 1; i < NUM_PIPES; ++i) begin
                mult_in1_q[i] <= mult_in1_q[i-1];
                signed_overflow[i] <= signed_overflow[i-1];
                divide_by_0[i] <= divide_by_0[i-1];
                sign_mult_in1[i] <= sign_mult_in1[i-1];
                funct3_q[i] <= funct3_q[i-1];
            end
        end
    end

    if (NUM_STAGE == 2) begin
        // multiplier (DW02_mult_2_stage) 33-bit multiplier
        DW02_mult_2_stage #(
            .A_width(XLEN + 1),
            .B_width(XLEN + 1)
        ) m_u (
            .CLK(clk_i),
            .TC(1'b1),
            .A(md_op1),
            .B(md_op2),
            .PRODUCT(mult_result)
        );
        // divider (DW02_div_pipe)
        DW_div_pipe #(
            .a_width(XLEN + 1),
            .b_width(XLEN + 1),
            .tc_mode(1'b1),
            .rem_mode(1'b1),
            .num_stages(NUM_STAGE),
            .stall_mode(1'b1)
        ) d_u (
            .clk(clk_i),
            .rst_n(rst_ni),
            .en(is_muldiv),
            .a(md_op1),
            .b(md_op2),
            .quotient(div_result),
            .remainder(rem_result),
            .divide_by_0()
        );
    end else if (NUM_STAGE == 3) begin
        // multiplier (DW02_mult_2_stage) 33-bit multiplier
        DW02_mult_3_stage #(
            .A_width(XLEN + 1),
            .B_width(XLEN + 1)
        ) m_u (
            .CLK(clk_i),
            .TC(1'b1),
            .A(md_op1),
            .B(md_op2),
            .PRODUCT(mult_result)
        );
        // divider (DW02_div_pipe)
        DW_div_pipe #(
            .a_width(XLEN + 1),
            .b_width(XLEN + 1),
            .tc_mode(1'b1),
            .rem_mode(1'b1),
            .num_stages(NUM_STAGE),
            .stall_mode(1'b1)
        ) d_u (
            .clk(clk_i),
            .rst_n(rst_ni),
            .en(is_muldiv),
            .a(md_op1),
            .b(md_op2),
            .quotient(div_result),
            .remainder(rem_result),
            .divide_by_0()
        );
    end

    assign mult_result_signed_unsigned = ~mult_result + 1'b1;

    // output logic 
    always @(*) begin
        result_o = '0;
        case (funct3_q[NUM_PIPES-1])
            `FUNCT3_MUL: begin
                result_o = mult_result[XLEN-1:0];
            end
            `FUNCT3_MULH: begin
                result_o = mult_result[XLEN+XLEN-1:XLEN];
            end    
            `FUNCT3_MULHSU: begin
                if (sign_mult_in1[NUM_PIPES-1]) begin
                    result_o = mult_result_signed_unsigned[XLEN+XLEN-1:XLEN];
                end else begin 
                    result_o = mult_result[XLEN+XLEN-1:XLEN];
                end
            end        
            `FUNCT3_MULHU: begin
                result_o = mult_result[XLEN+XLEN-1:XLEN];
            end
            `FUNCT3_DIV: begin
                if (signed_overflow[NUM_PIPES-1]) begin
                    result_o = mult_in1_q[NUM_PIPES-1];
                end else if (divide_by_0[NUM_PIPES-1]) begin
                    result_o = 32'hFFFFFFFF;
                end else begin
                    result_o = div_result[XLEN-1:0];
                end
            end
            `FUNCT3_DIVU: begin
                result_o = div_result[XLEN-1:0];
            end
            `FUNCT3_REM: begin
                if (signed_overflow[NUM_PIPES-1]) begin
                    result_o = 32'h0;
                end else begin
                    result_o = rem_result[XLEN-1:0];
                end
            end
            `FUNCT3_REMU: begin
                result_o = rem_result[XLEN-1:0];
            end
            default: begin
                result_o = '0;
            end
        endcase
    end

    // output valid shift
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            valid_counter <= '0;
        end else begin
            if (is_muldiv) begin
                valid_counter <= (valid_counter << 1) + 1'b1;
            end else begin
                valid_counter <= (valid_counter << 1) + 1'b0;
            end
        end
    end
    
    // output valid
    assign valid_o = valid_counter[NUM_PIPES-1];


endmodule