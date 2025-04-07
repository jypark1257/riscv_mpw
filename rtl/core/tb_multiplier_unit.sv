`timescale 1ps/1ps

module tb_multiplier_unit;

    localparam CLK_PERIOD = 4;

    logic clk;
    logic rst;
    logic [6:0] opcode;
    logic [6:0] funct7;
    logic [2:0] funct3;
    logic [31:0] mult_in1;
    logic [31:0] mult_in2;
    logic valid;

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars();
    end

    always begin
        #CLK_PERIOD; clk = ~clk;
    end


    multiplier_unit #(
        .NUM_STAGE(2)
    ) m_u (
        .clk_i(clk),
        .rst_ni(rst),
        .mult_in1_i(mult_in1),
        .mult_in2_i(mult_in2),
        .opcode_i(opcode),
        .funct7_i(funct7),
        .funct3_i(funct3),
        .result_o(),
        .valid_o(valid)
    ); 

    multiplier_unit_lyj m_u_lyj (
        .mult_in1_i(mult_in1),
        .mult_in2_i(mult_in2),
        .opcode_i(opcode),
        .funct7_i(funct7),
        .funct3_i(funct3),
        .result_o()
    ); 


    initial begin
        #0; rst = 0;
        #5; clk = 0; rst = 1;

        repeat(20) @(posedge clk);
         
        @(posedge clk); 
        mult_in1 = $random%10000000;
        mult_in2 = $random%10000000;
        opcode = 7'b01_100_11; funct7 = 7'h01; funct3 = 3'b011; 
        @(posedge clk); 
        mult_in1 = $random%10000000;
        mult_in2 = $random%10000000;
        opcode = 7'b01_100_11; funct7 = 7'h01; funct3 = 3'b011; 
        @(posedge clk); 
        mult_in1 = $random%10000000;
        mult_in2 = $random%10000000;
        opcode = 7'b01_100_11; funct7 = 7'h01; funct3 = 3'b011; 
        @(posedge clk); 
        mult_in1 = $random%10000000;
        mult_in2 = $random%10000000;
        opcode = 7'b01_100_11; funct7 = 7'h01; funct3 = 3'b011; 
        @(posedge clk); 
        mult_in1 = $random%10000000;
        mult_in2 = $random%10000000;
        opcode = 7'b01_100_11; funct7 = 7'h01; funct3 = 3'b011; 

        
        repeat(20) @(posedge clk);
        $finish;
    end



endmodule