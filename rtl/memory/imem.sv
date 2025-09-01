module imem #(
    parameter MEM_DEPTH = 4096,
    parameter MEM_ADDR_WIDTH = 14
) (
    input                   i_clk,

    input           [31:0]  i_instr_addr,
    output  logic   [31:0]  o_instr_rd_data,
    input           [31:0]  i_instr_wr_data,
    input           [3:0]   i_instr_size,
	input					i_instr_write,
	input					i_instr_read
);

	/* FPGA BRAM INSTANCE */
	ram_block_imem  #(
    	.IMEM_DEPTH(MEM_DEPTH),
    	.IMEM_ADDR_WIDTH(MEM_ADDR_WIDTH)
	) imem_sram(	
		.i_clk(i_clk),
		.i_addr(i_instr_addr[MEM_ADDR_WIDTH-1:0]),
		.i_we(i_instr_write),
		.i_size(i_instr_size),
		.i_din(i_instr_wr_data),
		.o_dout(o_instr_rd_data)
	);


	//sram_1024w_32b imem_sram (
	//	.CLK 			(i_clk),
	//	.CEN			(1'b0),
    //   .GWEN           (i_instr_read),
	//	.WEN			(~({4{i_instr_write}} & i_instr_size)),
	//	.A 				(i_instr_addr[MEM_ADDR_WIDTH-1:2]),     // 10-bit address
	//	.D 				(i_instr_wr_data),
	//	.EMA			(3'b000),
	//	.RETN			(1'b1),
	//	// outputs
	//	.Q 				(o_instr_rd_data)
	//);



endmodule