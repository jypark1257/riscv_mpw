
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
	output logic				SYNCRSTN,

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

	logic sync_spi_rst_n;
    logic sync_rv_rst_n;

	logic rv_rst_n[0:4];
	logic spi_rst_n[0:4];
	always_ff @(posedge CLK or negedge RVRSTN) begin
		if (RVRSTN == '0) begin
			rv_rst_n[0] <= '0;
			rv_rst_n[1] <= '0;
			rv_rst_n[2] <= '0;
			rv_rst_n[3] <= '0;
			rv_rst_n[4] <= '0;
		end else begin
			rv_rst_n[0] <= RVRSTN;
			rv_rst_n[1] <= rv_rst_n[0];
			rv_rst_n[2] <= rv_rst_n[1];
			rv_rst_n[3] <= rv_rst_n[2];
			rv_rst_n[4] <= rv_rst_n[3];
		end
	end
	assign sync_rv_rst_n = rv_rst_n[4];
	assign SYNCRSTN = sync_rv_rst_n;
    
	always_ff @(posedge CLK or negedge SPIRSTN) begin
		if (SPIRSTN == '0) begin
			spi_rst_n[0] <= '0;
			spi_rst_n[1] <= '0;
			spi_rst_n[2] <= '0;
			spi_rst_n[3] <= '0;
			spi_rst_n[4] <= '0;
		end else begin
			spi_rst_n[0] <= SPIRSTN;
			spi_rst_n[1] <= spi_rst_n[0];
			spi_rst_n[2] <= spi_rst_n[1];
			spi_rst_n[3] <= spi_rst_n[2];
			spi_rst_n[4] <= spi_rst_n[3];
		end	
	end
	assign sync_spi_rst_n = spi_rst_n[4];

    core_top #(
        .FPGA(FPGA),
        .XLEN(XLEN),
        .CPU_CLOCK_FREQ(CPU_CLOCK_FREQ),
        .RESET_PC(RESET_PC),
        .BAUD_RATE(BAUD_RATE)
    ) core_u (
        .clk_i(CLK),
        .rv_rst_ni(sync_rv_rst_n),
        .serial_rx_i(SERIALRX),
        .serial_tx_o(SERIALTX),
        .spi_rst_ni(sync_spi_rst_n),
        .sclk_i(SCLK),
        .cs_i(CS),
        .mosi_i(MOSI),
        .miso_o(MISO),
        .pim_addr_o(PIMADDR),
        .pim_wr_o(PIMWD),
        .pim_rd_i(PIMRD)
    );

endmodule
