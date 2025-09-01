
module core_top #(
    parameter bit FPGA          = 0,
    parameter XLEN              = 32,
    parameter CPU_CLOCK_FREQ    = 100_000_000,
    parameter RESET_PC          = 32'h1000_0000
) (
    input                       clk_i,
    // CORE RESET (SYNC)
    input                       rv_rst_ni,
    //UART 
	input						serial_rx_i,
	output logic				serial_tx_o,
	
	// SPI RESET (SYNC)
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
    logic [11:0]                dma_imm;
    logic [XLEN-1:0]            dma_rs1;
    logic [XLEN-1:0]            dma_rs2;
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

	logic serial_tx_orig;
	logic serial_rx_orig;
	logic serial_tx_test;
	logic serial_rx_test;

    // BUS rst_n
    assign sync_bus_rst_n = rv_rst_ni || spi_rst_ni;


	always_ff @(posedge clk_i or negedge spi_rst_ni) begin
		if(spi_rst_ni == '0) begin
			cs_reg <= '0;
		end else begin
			cs_reg <= cs_i;
		end
	end

    core #(
        .FPGA                   (FPGA),
        .RESET_PC               (RESET_PC)
    ) core_0 (
        .clk_i                  (clk_i),
        .rst_ni                 (rv_rst_ni),

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
        .dma_imm_o              (dma_imm),
        .dma_rs1_o              (dma_rs1),
        .dma_rs2_o              (dma_rs2)
    );

	pim_dma_v2 #(
        .PIM_BASE_ADDR          (32'h4000_0000),
        .PIM_MODE               (32'h4100_0000),
        .PIM_ZP_ADDR            (32'h4200_0000),
        .PIM_STATUS             (32'h4300_0000)
	) dma_0 (
        .clk_i                  (clk_i),
        .rst_ni                 (rv_rst_ni),
        // CORE interface
        .dma_en_i               (dma_en),
        .funct3_i               (dma_funct3),
        .imm_i                  (dma_imm),
        .rs1_i                  (dma_rs1),
        .rs2_i                  (dma_rs2),
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
        .rst_ni                 (sync_bus_rst_n),

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
        .rst_ni                 (spi_rst_ni),
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

    if (FPGA == 0) begin
        // IMEM
        logic [11:0] imem_addr_0;
        logic [11:0] imem_addr_1;
        logic [11:0] imem_addr_2;
        logic [11:0] imem_addr_3;
        logic [7:0] dout_0;
        logic [7:0] dout_1;
        logic [7:0] dout_2;
        logic [7:0] dout_3;
        assign imem_addr_0 = imem_addr[13:2] + |imem_addr[1:0];
        assign imem_addr_1 = imem_addr[13:2] + imem_addr[1];
        assign imem_addr_2 = imem_addr[13:2] + &imem_addr[1:0];
        assign imem_addr_3 = imem_addr[13:2];

        logic [31:0] imem_addr_q;
        logic [31:0] imem_rd_data_tmp;

        always_ff @(posedge clk_i or negedge rv_rst_ni) begin
            if (~rv_rst_ni) begin
                imem_addr_q <= '0;
            end else begin
                imem_addr_q <= imem_addr;
            end        
        end

        always @(*) begin
            case(imem_addr_q[1:0])
                2'b00: begin
                    imem_rd_data_tmp = {dout_3, dout_2, dout_1, dout_0};
                end
                2'b01: begin
                    imem_rd_data_tmp = {dout_0, dout_3, dout_2, dout_1};
                end
                2'b10: begin
                    imem_rd_data_tmp = {dout_1, dout_0, dout_3, dout_2};
                end
                2'b11: begin
                    imem_rd_data_tmp = {dout_2, dout_1, dout_0, dout_3};
                end
            endcase 
        end

        // IMEM
        sram_4096w_8b M0_0 (
		    .CLK 			(clk_i),
		    .CEN			(1'b0),
		    .WEN			(~({{imem_write}} & imem_size[0])),
		    .A 				(imem_addr_0), // 12-bit address
		    .D 				(imem_wr_data[7:0]),
		    .EMA			(3'b000),
		    .RETN			(1'b1),
		    // outputs
		    .Q 				(dout_0)
	    );
        sram_4096w_8b M0_1 (
		    .CLK 			(clk_i),
		    .CEN			(1'b0),
		    .WEN			(~({{imem_write}} & imem_size[1])),
		    .A 				(imem_addr_1), // 12-bit address
		    .D 				(imem_wr_data[15:8]),
		    .EMA			(3'b000),
		    .RETN			(1'b1),
		    // outputs
		    .Q 				(dout_1)
	    );
        sram_4096w_8b M0_2 (
		    .CLK 			(clk_i),
		    .CEN			(1'b0),
		    .WEN			(~({{imem_write}} & imem_size[2])),
		    .A 				(imem_addr_2), // 12-bit address
		    .D 				(imem_wr_data[23:16]),
		    .EMA			(3'b000),
		    .RETN			(1'b1),
		    // outputs
		    .Q 				(dout_2)
	    );
        sram_4096w_8b M0_3 (
		    .CLK 			(clk_i),
		    .CEN			(1'b0),
		    .WEN			(~({{imem_write}} & imem_size[3])),
		    .A 				(imem_addr_3), // 12-bit address
		    .D 				(imem_wr_data[31:24]),
		    .EMA			(3'b000),
		    .RETN			(1'b1),
		    // outputs
		    .Q 				(dout_3)
	    );
        assign imem_rd_data = imem_rd_data_tmp;
    
        // DMEM
        sram_4096w_32b M1_0 (
	    	.CLK 			(clk_i),
	    	.CEN			(1'b0),
            .GWEN           (dmem_read),
	    	.WEN			(~({4{dmem_write}} & dmem_size)),
	    	.A 				(dmem_addr[13:2]), // 12-bit address
	    	.D 				(dmem_wr_data),
	    	.EMA			(3'b000),
	    	.RETN			(1'b1),
	    	// outputs
	    	.Q 				(dmem_rd_data)
	    );

	    // BUF_0
        sram_4096w_32b M2_0 (
	    	.CLK 			(clk_i),
	    	.CEN			(1'b0),
            .GWEN           (buf_read_0),
	    	.WEN			(~({4{buf_write_0}} & buf_size_0)),
	    	.A 				(buf_addr_0[13:2]), // 12-bit address
	    	.D 				(buf_wr_data_0),
	    	.EMA			(3'b000),
	    	.RETN			(1'b1),
	    	// outputs
	    	.Q 				(buf_rd_data_0)
	    );
    
	    //// BUF_1
        //sram_4096w_32b_wrapper M2_1 (
        //    .clk_i          (clk_i),
        //    .gwen_i         (buf_read_1),
        //    .wen_i          (~({4{buf_write_1}} & buf_size_1)),
        //    .addr_i         (buf_addr_1[13:2]),
        //    .din_i          (buf_wr_data_1),
        //    .dout_o         (buf_rd_data_1)
        //);

    end else begin
        // IMEM
        imem #(
            .MEM_DEPTH              (4096),
            .MEM_ADDR_WIDTH         (14)
        ) imem_0 (
            .i_clk                  (clk_i),

            .i_instr_addr           (imem_addr),
            .o_instr_rd_data        (imem_rd_data),
            .i_instr_wr_data        (imem_wr_data),
            .i_instr_size           (imem_size),
            .i_instr_write          (imem_write),
            .i_instr_read           (imem_read)
        );

        // DMEM
        dmem #(
            .MEM_DEPTH              (4096),
            .MEM_ADDR_WIDTH         (14)
        ) dmem_0 (
            .i_clk                  (clk_i),

            .i_data_addr            (dmem_addr),
            .o_data_rd_data         (dmem_rd_data),
            .i_data_wr_data         (dmem_wr_data),
            .i_data_size            (dmem_size),
            .i_data_write           (dmem_write),
            .i_data_read            (dmem_read)
        );

        // weight and activation buffer
        pim_buffer #(
            .MEM_DEPTH              (16384),
            .MEM_ADDR_WIDTH         (14)
        ) buf_0 (
            .i_clk                  (clk_i),

            .i_buf_addr             (buf_addr_0),
            .o_buf_rd_data          (buf_rd_data_0),
            .i_buf_wr_data          (buf_wr_data_0),
            .i_buf_size             (buf_size_0),
            .i_buf_write            (buf_write_0),
            .i_buf_read             (buf_read_0)
        );

        pim_buffer #(
            .MEM_DEPTH              (16384),
            .MEM_ADDR_WIDTH         (14)
        ) buf_1 (
            .i_clk                  (clk_i),

            .i_buf_addr             (buf_addr_1),
            .o_buf_rd_data          (buf_rd_data_1),
            .i_buf_wr_data          (buf_wr_data_1),
            .i_buf_size             (buf_size_1),
            .i_buf_write            (buf_write_1),
            .i_buf_read             (buf_read_1)
        );
    
    end

    // on-chip uart
    uart_wrap_test #(
        .UART_CTRL              (32'h8000_0000),
        .UART_RECV              (32'h8000_0004),
        .UART_TRANS             (32'h8000_0008),
        .UART_SYMBOL_EDGE_TIME  (32'h8000_000C),
        .UART_SAMPLE_TIME       (32'h8000_0010)
    ) on_chip_uart_0 (
        .clk_i                  (clk_i), 
        .rst_ni                 (rv_rst_ni), 
        .uart_addr_i            (uart_addr),
        .uart_write_i           (uart_write),
        .uart_read_i            (uart_read),
        .uart_size_i            (uart_size),
        .uart_din_i             (uart_wr_data),
        .uart_dout_o            (uart_rd_data),
        .serial_rx_i            (serial_rx_orig),
        .serial_tx_o            (serial_tx_orig)
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
	always_ff @(posedge clk_i or negedge rv_rst_ni) begin
		if (rv_rst_ni == '0) begin
			serial_tx_o <= '0;
			serial_rx_orig <= '0;
		end else begin
			    serial_tx_o <= serial_tx_orig;
			    serial_rx_orig <= serial_rx_i;
		end
	end

	

endmodule
