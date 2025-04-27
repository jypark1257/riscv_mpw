


module mpw_top (
    input                       i_clk,
    // CORE RESET
    input                       i_rv_rst_n,
    
    // SPI RESET
    input                       i_spi_rst_n,

    // SPI
    input                       sclk,
    input                       cs,
    input                       mosi,
    output logic                miso,

    // UART
    input                       i_serial_rx,
    output logic                o_serial_tx,

	output logic 				o_sync_rst_n

);

    logic [31:0] pim_addr;
    logic [31:0] pim_wr_data;
    logic [31:0] pim_rd_data;

    core_top #(
        .XLEN(32),
        .CPU_CLOCK_FREQ(250_000_000),
        .RESET_PC(32'h1000_0000),
        .BAUD_RATE(115200)
    ) core_top_0 (
        .CLK				(i_clk),
        // CORE RESET
        .RVRSTN		        (i_rv_rst_n),
        
        // SPI RESET
        .SPIRSTN			(i_spi_rst_n),
    
        // SPI
        .SCLK	            (sclk),
        .CS					(cs),
        .MOSI				(mosi),
        .MISO				(miso),
    
        // UART
		.SERIALRX					(i_serial_rx),
        .SERIALTX					(o_serial_tx),
		.SYNCRSTN			(o_sync_rst_n),
    
        // PIM I/F
        .PIMADDR			(pim_addr),
        .PIMWD				(pim_wr_data),
        .PIMRD				(pim_rd_data)
    );

    PIM_TOP pim_top_0 (
        .CLK(i_clk),
        .RSTN(o_sync_rst_n),

        .i_address(pim_addr),
        .i_data(pim_wr_data),
        .o_data(pim_rd_data)
    );


endmodule

