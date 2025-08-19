
module ram_block_dmem #(	
    parameter DMEM_DEPTH = 4096,		// dmem depth in a word (4 bytes, default: 1024 entries = 4 KB)
	parameter DMEM_ADDR_WIDTH = 12
) (
	input			                i_clk,

    input	[DMEM_ADDR_WIDTH-1:0]	i_addr,
	input							i_write,
	input							i_read,
	input	[3:0]	                i_size,	// data size (LB, LH, LW)
	input	[31:0]	                i_din,
	output	[31:0]	                o_dout
);

	// memory entries. dmem is split into 4 banks to support various data granularity
	(* ram_style="block" *) logic	[7:0]	d0[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d1[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d2[0:DMEM_DEPTH-1];
	(* ram_style="block" *) logic	[7:0]	d3[0:DMEM_DEPTH-1];

    initial begin
        $readmemh("dmem_0.mem", d0);
        $readmemh("dmem_1.mem", d1);
        $readmemh("dmem_2.mem", d2);
        $readmemh("dmem_3.mem", d3);
    end

    // address for each bank
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_0;	// address for bank 0
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_1;	// address for bank 1
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_2;	// address for bank 2
	logic	[DMEM_ADDR_WIDTH-3:0]	addr_3;	// address for bank 3
	
	assign addr_0 = i_addr[DMEM_ADDR_WIDTH-1:2];
	assign addr_1 = i_addr[DMEM_ADDR_WIDTH-1:2];
	assign addr_2 = i_addr[DMEM_ADDR_WIDTH-1:2];
	assign addr_3 = i_addr[DMEM_ADDR_WIDTH-1:2];
	
	// data out from each bank
	logic	[7:0]	dout_0, dout_1, dout_2, dout_3;
	
    always_ff @(posedge i_clk) begin
		if (i_read) begin
        	dout_0 <= d0[addr_0];
        	dout_1 <= d1[addr_1];
        	dout_2 <= d2[addr_2];
        	dout_3 <= d3[addr_3];
		end
    end
	
	assign o_dout = {dout_3, dout_2, dout_1, dout_0};
	
	// in the textbook, dmem does not receive the clock signal
	// but clocked write operation is required for better operation and synthesis
	// we must avoid latch for the normal cases
	always_ff @ (posedge i_clk) begin
		if ((i_size[0] && i_write)) d0[addr_0] <= i_din[7:0];
		if ((i_size[1] && i_write)) d1[addr_1] <= i_din[15:8];
		if ((i_size[2] && i_write)) d2[addr_2] <= i_din[23:16];
		if ((i_size[3] && i_write)) d3[addr_3] <= i_din[31:24];
	end

endmodule