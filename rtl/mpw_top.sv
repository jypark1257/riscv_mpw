
module mpw_top #(
    parameter bit FPGA           = 0,
    parameter XLEN              = 32,
    parameter CPU_CLOCK_FREQ    = 250_000_000,
    parameter RESET_PC          = 32'h1000_0000,
    parameter BAUD_RATE         = 115200
) (
    input                       CLK,
    // CORE RESET
    input                       RVRSTN,
	// SYNC RESET
	output						SYNCRSTN,

    // UART SELECT
    input                       orig_test_switch,

    //UART 
	input						SERIALRX,
	output logic				SERIALTX,
	
	// SPI RESET
    input                       SPIRSTN,
    // SPI
    input                       SCLK,
    input                       CS,
    input                       MOSI,
    output logic                MISO,

    // PIM I/F
    output logic    [XLEN-1:0]  PIMADDR,
    output logic    [XLEN-1:0]  PIMWD,
    input           [XLEN-1:0]	PIMRD
);

    core_top #(
        .FPGA(FPGA)
        .XLEN(XLEN),
        .CPU_CLOCK_FREQ(CPU_CLOCK_FREQ),
        .RESET_PC(RESET_PC),
        .BAUD_RATE(BAUD_RATE)
    ) core_u (
        .clk_i(CLK),
        .rv_rst_ni(RVRSTN),
        .sync_rst_no(SYNCRSTN),
        .orig_test_switch(orig_test_switch),
        .serial_rx_i(SERIALRX),
        .serial_tx_o(SERIALTX),
        .spi_rst_ni(SPIRSTN),
        .sclk_i(SCLK),
        .cs_i(CS),
        .mosi_i(MOSI),
        .miso_o(MISO),
        .pim_addr_o(PIMADDR),
        .pim_wr_o(PIMWD),
        .pim_rd_i(PIMRD)
    );

endmodule
