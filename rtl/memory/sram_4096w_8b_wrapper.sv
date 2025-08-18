

module sram_4096w_8b_wrapper (
    input logic clk_i,
    input logic wen_i,
    input logic [11:0] addr_i,
    input logic [7:0] din_i,
    output logic [7:0] dout_o
);
    sram_4096w_8b SRAM_4096W_8B (
		.CLK 			(clk_i),
		.CEN			(1'b0),
		.WEN			(wen_i),
		.A 				(addr_i), // 12-bit address
		.D 				(din_i),
		.EMA			(3'b000),
		.RETN			(1'b1),
		// outputs
		.Q 				(dout_o)
	);
endmodule