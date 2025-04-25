module dmem #(
    parameter MEM_DEPTH = 4096,
    parameter MEM_ADDR_WIDTH = 12
) (
    input                   i_clk,
    
    input           [31:0]  i_data_addr,
    output  logic   [31:0]  o_data_rd_data,
    input           [31:0]  i_data_wr_data,
    input           [3:0]   i_data_size,
	input					i_data_write,
	input					i_data_read
);

	/* FPGA BRAM INSTANCE */
	ram_block_dmem  #(
    	.DMEM_DEPTH(MEM_DEPTH),
    	.DMEM_ADDR_WIDTH(MEM_ADDR_WIDTH)
	)  dmem_sram(	
		.i_clk(i_clk),
		.i_addr({i_data_addr[MEM_ADDR_WIDTH-1:2], 2'b00}),
		.i_write(i_data_write),
    	.i_read(i_data_read),
		.i_size(i_data_size),
		.i_din(i_data_wr_data),
		.o_dout(o_data_rd_data)
	);	


	//sram_1024w_32b dmem_sram (
	//	.CLK 			(i_clk),
	//	.CEN			(1'b0),
    //    .GWEN           (i_data_read),
	//	.WEN			(~({4{i_data_write}} & i_data_size)),
	//	.A 				(i_data_addr[MEM_ADDR_WIDTH-1:2]),
	//	.D 				(i_data_wr_data),
	//	.EMA			(3'b000),
	//	.RETN			(1'b1),
	//	// outputs
	//	.Q 				(o_data_rd_data)
	//);


endmodule