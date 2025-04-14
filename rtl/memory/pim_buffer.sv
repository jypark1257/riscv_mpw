module pim_buffer #(
    parameter MEM_DEPTH = 28672,	//28KB
    parameter MEM_ADDR_WIDTH = 15
) (
    input                   i_clk,

    input           [31:0]  i_buf_addr,
    output  logic   [31:0]  o_buf_rd_data,
    input           [31:0]  i_buf_wr_data,
    input           [3:0]   i_buf_size,
	input					i_buf_write,
	input					i_buf_read
);
	/* FPGA INSTANCE */
	ram_block_buf #(
        .DMEM_DEPTH(MEM_DEPTH),
        .DMEM_ADDR_WIDTH(MEM_ADDR_WIDTH)
    ) buf_sram (	
		.i_clk(i_clk),
		.i_addr({i_buf_addr[MEM_ADDR_WIDTH-1:2], 2'b00}),
		.i_write(i_buf_write),
		.i_read(i_buf_read),
		.i_size(i_buf_size),
		.i_din(i_buf_wr_data),
		.o_dout(o_buf_rd_data)
	);	

endmodule