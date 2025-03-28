
module core_top #(
    parameter XLEN              = 32,
    parameter CPU_CLOCK_FREQ    = 250_000_000,
    parameter RESET_PC          = 32'h1000_0000,
    parameter BAUD_RATE         = 115200
) (
    input                       clk_i,
    // CORE RESET
    input                       rv_rst_ni,
	// SYNC RESET
	output						sync_rst_no,
    //UART 
	input						serial_rx_i,
	output logic				serial_tx_o,
	
	// SPI RESET
    input                       spi_rst_ni,
    // SPI
    input                       sclk_i,
    input                       cs_i,
    input                       mosi_i,
    output logic                miso_o,

    // PIM I/F
    output logic    [XLEN-1:0]  pim_addr_o,
    output logic    [XLEN-1:0]  pim_wr_o,
    input           [XLEN-1:0]	pim_rd_i
);
	
	logic						cs_reg;

	logic						sync_spi_rst_n;
    logic                       sync_rv_rst_n;
    logic                       sync_bus_rst_n;


    // SPI I/F
    logic                       req_spi;
    logic                       gnt_spi;
    logic [XLEN-1:0]            spi_addr;
    logic [XLEN-1:0]            spi_rd_data;
    logic [XLEN-1:0]            spi_wr_data;
    logic [3:0]                 spi_size;
    logic                       spi_read;
    logic                       spi_write;

    // RV IMEM I/F
    logic [XLEN-1:0]            instr_addr;
    logic [XLEN-1:0]            instr_rd_data;
    logic [XLEN-1:0]            instr_wr_data;
    logic [3:0]                 instr_size;
    logic                       instr_read;
    logic                       instr_write;

    // RV DMEM I/F
    logic                       req_data;
    logic                       gnt_data;
    logic [XLEN-1:0]            data_addr;
    logic [XLEN-1:0]            data_rd_data;
    logic [XLEN-1:0]            data_wr_data;
    logic [3:0]                 data_size;
    logic                       data_read;
    logic                       data_write;

    // SRAM IMEM I/F
    logic [XLEN-1:0]            imem_addr;
    logic [XLEN-1:0]            imem_rd_data;
    logic [XLEN-1:0]            imem_wr_data;
    logic [3:0]                 imem_size;
    logic                       imem_read;
    logic                       imem_write;

    // SRAM DMEM I/F
    logic [XLEN-1:0]            dmem_addr;
    logic [XLEN-1:0]            dmem_rd_data;
    logic [XLEN-1:0]            dmem_wr_data;
    logic [3:0]                 dmem_size;  
    logic                       dmem_read;
    logic                       dmem_write;
 
    // UART
    logic [XLEN-1:0]            uart_addr;
    logic [XLEN-1:0]            uart_rd_data;
    logic [XLEN-1:0]            uart_wr_data;
    logic [3:0]                 uart_size;  
    logic                       uart_read;
    logic                       uart_write;

    // PIM BUFFER I/F
    logic [XLEN-1:0]            pim_addr;
    logic [XLEN-1:0]            pim_rd_data;
    logic [XLEN-1:0]            pim_wr_data;
    logic [3:0]                 pim_size;  
    logic                       pim_read;
    logic                       pim_write;

    // DMA
    logic                       dma_en;
    logic                       req_dma;
    logic                       gnt_dma;
    logic [2:0]                 dma_funct3;
    logic [3:0]                 dma_sel_pim;
    logic [12:0]                dma_trans_size;
    logic [XLEN-1:0]            dma_mem_addr;
    logic [XLEN-1:0]            dma_addr_0;
    logic                       dma_write_0;
    logic                       dma_read_0;
    logic [3:0]                 dma_size_0;  
    logic [XLEN-1:0]            dma_rd_data_0;
    logic [XLEN-1:0]            dma_wr_data_0;
    logic [XLEN-1:0]            dma_addr_1;
    logic                       dma_write_1;
    logic                       dma_read_1;
    logic [3:0]                 dma_size_1;  
    logic [XLEN-1:0]            dma_rd_data_1;
    logic [XLEN-1:0]            dma_wr_data_1;
    logic                       dma_busy;

	// 16KB mem 0
	logic [XLEN-1:0]			buf_addr_0;
	logic [XLEN-1:0]			buf_rd_data_0;
	logic [XLEN-1:0]			buf_wr_data_0;
	logic [3:0]					buf_size_0;
	logic						buf_read_0;
	logic						buf_write_0;
	// 16KB mem 1
	logic [XLEN-1:0]			buf_addr_1;
	logic [XLEN-1:0]			buf_rd_data_1;
	logic [XLEN-1:0]			buf_wr_data_1;
	logic [3:0]					buf_size_1;
	logic						buf_read_1;
	logic						buf_write_1;

	logic serial_tx;
	logic serial_rx;

	logic rv_rst_n[0:4];
	logic spi_rst_n[0:4];
	always_ff @(posedge clk_i or negedge rv_rst_ni) begin
		if (rv_rst_ni == '0) begin
			rv_rst_n[0] <= '0;
			rv_rst_n[1] <= '0;
			rv_rst_n[2] <= '0;
			rv_rst_n[3] <= '0;
			rv_rst_n[4] <= '0;
		end else begin
			rv_rst_n[0] <= rv_rst_ni;
			rv_rst_n[1] <= rv_rst_n[0];
			rv_rst_n[2] <= rv_rst_n[1];
			rv_rst_n[3] <= rv_rst_n[2];
			rv_rst_n[4] <= rv_rst_n[3];
		end
	end
	assign sync_rv_rst_n = rv_rst_n[4];
	assign sync_rst_no = sync_rv_rst_n;
    
	always_ff @(posedge clk_i or negedge spi_rst_ni) begin
		if (spi_rst_ni == '0) begin
			spi_rst_n[0] <= '0;
			spi_rst_n[1] <= '0;
			spi_rst_n[2] <= '0;
			spi_rst_n[3] <= '0;
			spi_rst_n[4] <= '0;
		end else begin
			spi_rst_n[0] <= spi_rst_ni;
			spi_rst_n[1] <= spi_rst_n[0];
			spi_rst_n[2] <= spi_rst_n[1];
			spi_rst_n[3] <= spi_rst_n[2];
			spi_rst_n[4] <= spi_rst_n[3];
		end	
	end
	assign sync_spi_rst_n = spi_rst_n[4];


    // BUS rst_n
    assign sync_bus_rst_n = sync_rv_rst_n || sync_spi_rst_n;


	always_ff @(posedge clk_i or negedge sync_spi_rst_n) begin
		if(sync_spi_rst_n == '0) begin
			cs_reg <= '0;
		end else begin
			cs_reg <= cs_i;
		end
	end

    core #(
        .RESET_PC               (RESET_PC)
    ) core_0 (
        .clk_i                  (clk_i),
        .rst_ni                (sync_rv_rst_n),

        // instruction interface
        .instr_addr_o           (instr_addr),
        .instr_rd_data_i        (instr_rd_data),
        .instr_wr_data_o        (instr_wr_data),
        .instr_size_o           (instr_size),
        .instr_read_o           (instr_read),
        .instr_write_o          (instr_write),

        // data interface
        .req_dmem_o             (req_data),
        .gnt_dmem_i             (gnt_data),
        .data_addr_o            (data_addr),
        .data_rd_data_i         (data_rd_data),
        .data_wr_data_o         (data_wr_data),
        .data_size_o            (data_size),
        .data_read_o            (data_read),
        .data_write_o           (data_write),

        // dma status
        .dma_busy_i             (dma_busy),

        // dma interface
        .dma_en_o               (dma_en),
        .dma_funct3_o           (dma_funct3),
        .dma_sel_pim_o          (dma_sel_pim),
        .dma_size_o             (dma_trans_size),
        .dma_mem_addr_o         (dma_mem_addr)
    );

	pim_dma #(
        .PIM_CTRL               (32'h4000_0010),
        .PIM_R                  (32'h4000_0020),
        .PIM_W_WEIGHT           (32'h4000_0040),
        .PIM_W_ACTIVATION       (32'h4000_0080),
		.PIM_W_KEY				(32'h4000_0100),
		.PIM_W_VREF				(32'h4000_0200),
		.PIM_W_MODE				(32'h4000_0400)
	) dma_0 (
        .clk_i                  (clk_i),
        .rst_ni                 (sync_rv_rst_n),
        // CORE interface
        .dma_en_i               (dma_en),
        .funct3_i               (dma_funct3),
        .sel_pim_i              (dma_sel_pim),
        .size_i                 (dma_trans_size),      
        .mem_addr_i             (dma_mem_addr),
        // BUS interface
        .bus_req_o              (req_dma),
        .bus_gnt_i              (gnt_dma),
        .dma_addr_0_o           (dma_addr_0),
        .dma_write_0_o          (dma_write_0),
        .dma_read_0_o           (dma_read_0),
        .dma_size_0_o           (dma_size_0),
        .dma_wr_data_0_o        (dma_wr_data_0),
        .dma_rd_data_0_i        (dma_rd_data_0),
        .dma_addr_1_o           (dma_addr_1),
        .dma_write_1_o          (dma_write_1),
        .dma_read_1_o           (dma_read_1),
        .dma_size_1_o           (dma_size_1),
        .dma_wr_data_1_o        (dma_wr_data_1),
        .dma_rd_data_1_i        (dma_rd_data_1),
        // busy signal
        .dma_busy_o             (dma_busy)
    );


    // IDS BUS
    sys_bus bus_0 (
        .clk_i                  (clk_i), 
        .rst_ni                (sync_bus_rst_n),

    // MASTERS
    // RV IMEM
        .imem_addr_i            (instr_addr),
        .imem_write_i           (instr_write),
        .imem_read_i            (instr_read),
        .imem_size_i            (instr_size),
        .imem_din_i             (instr_wr_data),
        .imem_dout_o            (instr_rd_data),

    // SPI SLAVE
        .req_spi_i              (req_spi),
        .gnt_spi_o              (gnt_spi),
        .spi_addr_i             (spi_addr),
        .spi_write_i            (spi_write),
        .spi_read_i             (spi_read),
        .spi_size_i             (spi_size),
        .spi_din_i              (spi_wr_data),
        .spi_dout_o             (spi_rd_data),

    // RV DMEM
        .req_dmem_i             (req_data),
        .gnt_dmem_o             (gnt_data),
        .dmem_addr_i            (data_addr),
        .dmem_write_i           (data_write),
        .dmem_read_i            (data_read),
        .dmem_size_i            (data_size),
        .dmem_din_i             (data_wr_data),
        .dmem_dout_o            (data_rd_data),

    // DMA
        .req_dma_i              (req_dma),
        .gnt_dma_o              (gnt_dma),
        .dma_addr_0_i           (dma_addr_0),
        .dma_write_0_i          (dma_write_0),
        .dma_read_0_i           (dma_read_0),
        .dma_size_0_i           (dma_size_0),
        .dma_din_0_i            (dma_wr_data_0),
        .dma_dout_0_o           (dma_rd_data_0),
        .dma_addr_1_i           (dma_addr_1),
        .dma_write_1_i          (dma_write_1),
        .dma_read_1_i           (dma_read_1),
        .dma_size_1_i           (dma_size_1),
        .dma_din_1_i            (dma_wr_data_1),
        .dma_dout_1_o           (dma_rd_data_1),

    // SLAVES
    // IMEM SRAM (IMEM port)
        .imem_addr_o            (imem_addr),
        .imem_write_o           (imem_write),
        .imem_read_o            (imem_read),
        .imem_size_o            (imem_size),
        .imem_din_o             (imem_wr_data),
        .imem_dout_i            (imem_rd_data),

    // DMEM SRAM (DMEM port)
        .dmem_addr_o            (dmem_addr),
        .dmem_write_o           (dmem_write),
        .dmem_read_o            (dmem_read),
        .dmem_size_o            (dmem_size),
        .dmem_din_o             (dmem_wr_data),
        .dmem_dout_i            (dmem_rd_data),

    // PIM BUFFER SRAM
        .buf_addr_0_o           (buf_addr_0),
        .buf_write_0_o          (buf_write_0),
        .buf_read_0_o			(buf_read_0),
        .buf_size_0_o           (buf_size_0),
        .buf_din_0_o            (buf_wr_data_0),
        .buf_dout_0_i           (buf_rd_data_0),

        .buf_addr_1_o           (buf_addr_1),
        .buf_write_1_o          (buf_write_1),
        .buf_read_1_o			(buf_read_1),
        .buf_size_1_o           (buf_size_1),
        .buf_din_1_o            (buf_wr_data_1),
        .buf_dout_1_i           (buf_rd_data_1),



    // UART
        .uart_addr_o            (uart_addr),
        .uart_write_o           (uart_write),
        .uart_read_o            (uart_read),
        .uart_size_o            (uart_size),
        .uart_din_o             (uart_wr_data),
        .uart_dout_i            (uart_rd_data),

    // PIM
        .pim_addr_o             (pim_addr),
        .pim_write_o            (pim_write),
        .pim_read_o             (pim_read),
        .pim_size_o             (pim_size),
        .pim_din_o              (pim_wr_data),
        .pim_dout_i             (pim_rd_data)
    );

    // SPI SLAVE
    spi_slave_wrap spi_slave_0 (
        .clk_i                  (clk_i),
        .rst_ni                 (sync_spi_rst_n),
        // BUS I/F
        .req_spi_o              (req_spi),
        .gnt_spi_i              (gnt_spi),
        .spi_addr_o             (spi_addr),
        .spi_rd_data_i          (spi_rd_data),
        .spi_wr_data_o          (spi_wr_data),
        .spi_size_o             (spi_size),
        .spi_read_o             (spi_read),
        .spi_write_o            (spi_write),
        // SPI I/F
        .sclk_i                 (sclk_i),
        .cs_i                   (cs_reg),
        .mosi_i                 (mosi_i),
        .miso_o                 (miso_o)
    );

    // IMEM
    sram_1024w_32b M0_0 (
		.CLK 			(clk_i),
		.CEN			(1'b0),
        .GWEN           (imem_read),
		.WEN			(~({4{imem_write}} & imem_size)),
		.A 				(imem_addr[11:2]),     // 10-bit address
		.D 				(imem_wr_data),
		.EMA			(3'b000),
		.RETN			(1'b1),
		// outputs
		.Q 				(imem_rd_data)
	);

    // DMEM
    sram_1024w_32b M0_1 (
		.CLK 			(clk_i),
		.CEN			(1'b0),
        .GWEN           (dmem_read),
		.WEN			(~({4{dmem_write}} & dmem_size)),
		.A 				(dmem_addr[11:2]),
		.D 				(dmem_wr_data),
		.EMA			(3'b000),
		.RETN			(1'b1),
		// outputs
		.Q 				(dmem_rd_data)
	);

	// BUF_0
	sram_4096w_32b M1_0 (
		.CLK			(clk_i),
		.CEN			(1'b0),
		.GWEN			(buf_read_0),
		.WEN			(~({4{buf_write_0}} & buf_size_0)),
		.A				(buf_addr_0[13:2]),
		.D				(buf_wr_data_0),
		.EMA			(3'b000),
		.RETN			(1'b1),
		// outputs	
		.Q				(buf_rd_data_0)
	);

	// BUF_1
	sram_4096w_32b M1_1 (
		.CLK			(clk_i),
		.CEN			(1'b0),
		.GWEN			(buf_read_1),
		.WEN			(~({4{buf_write_1}} & buf_size_1)),
		.A				(buf_addr_1[13:2]),
		.D				(buf_wr_data_1),
		.EMA			(3'b000),
		.RETN			(1'b1),
		// outputs
		.Q				(buf_rd_data_1)
	);



    // on-chip uart
    uart_wrap #(
        .CLOCK_FREQ             (CPU_CLOCK_FREQ),
        .BAUD_RATE              (BAUD_RATE),
        .UART_CTRL              (32'h8000_0000),
        .UART_RECV              (32'h8000_0004),
        .UART_TRANS             (32'h8000_0008)
    ) on_chip_uart (
        .clk_i                  (clk_i), 
        .rst_ni                (sync_rv_rst_n), 
        .uart_addr_i            (uart_addr),
        .uart_write_i           (uart_write),
        .uart_read_i            (uart_read),
        .uart_size_i            (uart_size),
        .uart_din_i             (uart_wr_data),
        .uart_dout_o            (uart_rd_data),
        .serial_rx_i            (serial_rx),
        .serial_tx_o            (serial_tx)
    );

	// PIM controller INPUT/OUTPUT
	always_ff @(posedge clk_i or negedge sync_bus_rst_n) begin
		if (sync_bus_rst_n == '0) begin
			pim_addr_o <= '0;
			pim_wr_o <= '0;
		end else begin
			pim_addr_o <= pim_addr;
			pim_wr_o <= pim_wr_data;
		end
	end

    assign pim_rd_data = pim_rd_i;

	// UART INPUT/OUTPUT
	always_ff @(posedge clk_i or negedge sync_rv_rst_n) begin
		if (sync_rv_rst_n == '0) begin
			serial_tx_o <= '0;
			serial_rx <= '0;
		end else begin
			serial_rx <= serial_rx_i;
			serial_tx_o <= serial_tx;
		end
	end

	

endmodule
