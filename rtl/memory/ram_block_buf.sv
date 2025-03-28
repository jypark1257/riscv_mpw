
module ram_block_buf #(	
    parameter DMEM_DEPTH = 1024,		// dmem depth in a word (4 bytes, default: 1024 entries = 4 KB)
	parameter DMEM_ADDR_WIDTH = 12
) (
	input			                clk_i,

    input	[DMEM_ADDR_WIDTH-1:0]	addr_i,
	input							write_i,
	input							read_i,
	input	[3:0]	                size_i,	// data size (LB, LH, LW)
	input	[31:0]	                din_i,
	output	[31:0]	                dout_o
);

	// memory entries. dmem is split into 4 banks to support various data granularity
	(* ram_style="block" *) logic	[7:0]	d0[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d1[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d2[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d3[0:DMEM_DEPTH-1];

    // address for each bank
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_0;	// address for bank 0
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_1;	// address for bank 1
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_2;	// address for bank 2
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_3;	// address for bank 3
	
	assign addr_0 = addr_i[DMEM_ADDR_WIDTH-1:2];
	assign addr_1 = addr_i[DMEM_ADDR_WIDTH-1:2];
	assign addr_2 = addr_i[DMEM_ADDR_WIDTH-1:2];
	assign addr_3 = addr_i[DMEM_ADDR_WIDTH-1:2];
	
	// data out from each bank
	logic	[7:0]	dout_0, dout_1, dout_2, dout_3;
	
    always_ff @(posedge clk_i) begin
		if (read_i) begin
        	dout_0 <= d0[addr_0];
        	dout_1 <= d1[addr_1];
        	dout_2 <= d2[addr_2];
        	dout_3 <= d3[addr_3];
		end
    end
	
	assign dout_o = {dout_3, dout_2, dout_1, dout_0};
	
	// in the textbook, dmem does not receive the clock signal
	// but clocked write operation is required for better operation and synthesis
	// we must avoid latch for the normal cases
	always_ff @ (posedge clk_i) begin
		if ((size_i[0] && write_i)) d0[addr_0] <= din_i[7:0];
		if ((size_i[1] && write_i)) d1[addr_1] <= din_i[15:8];
		if ((size_i[2] && write_i)) d2[addr_2] <= din_i[23:16];
		if ((size_i[3] && write_i)) d3[addr_3] <= din_i[31:24];
	end

endmodule