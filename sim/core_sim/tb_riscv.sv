`timescale 1ns/10ps

module mpw_sim;

    parameter CLK_PERIOD = 10;
    parameter CLK_FREQ = 100_000_000;
    parameter BAUD_RATE = 115200;

    reg i_clk;
    reg i_rv_rst_n;
    reg i_spi_rst_n;
    reg o_sync_rst_n;

    reg [7:0] uart_data_in;
    reg uart_data_in_valid;
    wire uart_data_in_ready;
    wire [7:0] uart_data_out;
    wire uart_data_out_valid;
    reg uart_data_out_ready;
    wire serial_in;
    wire serial_out;

    wire sclk;
    wire mosi;
    wire miso;
    wire cs;
    reg spi_start;
    wire spi_done;
    reg [7:0] spi_data_in;
    reg [31:0] program_array [0:(4096 *2)-1];
    reg [31:0] flash_addr;


    // RISC-V <-> PERI
    wire [31:0] pim_addr;
    wire [31:0] pimwd;
    wire [31:0] pimrd;

    // PERI <-> PIM
    reg [1023:0] eFlash_output1_i;
    reg [1023:0] eFlash_output2_i;
    // Row wise signal
    wire [1:0] MODE_o;
    wire [127:0] WL_SEL_o;
    wire [127:0] VPASS_EN_o;

    wire [7:0] DUML_o;
    wire [7:0] CSL_o;
    wire [31:0] BSEL_o;
    wire [7:0] CSEL_o;
    wire ADC_EN1_o;
    wire ADC_EN2_o;
    wire QDAC_o;
    wire [1:0] RSEL_o;

    // Col wise signal
    wire [255:0] DUMH_o;
    wire [127:0] PRECB_o;
    wire [127:0] DISC_o;


	// string to be transfer
	string str;

    reg [7:0] uart_buffer [0:2048];
    integer uart_buffer_index;
    reg response_ready;

	initial begin
	    $dumpfile("wave.vcd");  // any file name possible
	    $dumpvars(0, mpw_sim);        // instance name required
	end

    // DUTs
    uart #(
        .CLOCK_FREQ(CLK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) uart_tb_0 (
        .clk(i_clk),
        .reset(!o_sync_rst_n),
        .data_in(uart_data_in),
        .data_in_valid(uart_data_in_valid),
        .data_in_ready(uart_data_in_ready),
        .data_out(uart_data_out),
        .data_out_valid(uart_data_out_valid),
        .data_out_ready(uart_data_out_ready),
        .serial_in(serial_out),
        .serial_out(serial_in)
    );

    spi_master spi_m_0 (
        .clk(i_clk),
        .rst_n(i_spi_rst_n),
        .start(spi_start),
        .done(spi_done),
        .data_in(spi_data_in),
        .data_out(),
        .sclk(sclk),
        .mosi(mosi),
        .miso(miso),
        .cs_n(cs)
    );

    mpw_top mpw_top_0 (
        .CLK(i_clk),
        .RVRSTN(i_rv_rst_n),
        .SPIRSTN(i_spi_rst_n),
        .SCLK(sclk),
        .CS(cs),
        .MOSI(mosi),
        .MISO(miso),
        .SERIALRX(serial_in),
        .SERIALTX(serial_out),
        .SYNCRSTN(o_sync_rst_n),
        .PIMADDR(pim_addr),
        .PIMRD(pimrd),  // Not used in this simulation
        .PIMWD(pimwd)
    );

    // instance here: PIM peripheral
    peri_top peri (
        .clk_i(i_clk),
        .rst_ni(i_rv_rst_n),

        // RISC-V
        .address_i(pim_addr),
        .data_i(pimwd),

        .data_o(pimrd),

        // PIM
        .eFlash_output_1_i(eFlash_output1_i),
        .eFlash_output_2_i(eFlash_output2_i),

        // Row wise signal
        .MODE_o(MODE_o),
        .WL_SEL_o(WL_SEL_o),
        .VPASS_EN_o(VPASS_EN_o),

        .DUML_o(DUML_o),
        .CSL_o(CSL_o),
        .BSEL_o(BSEL_o),
        .CSEL_o(CSEL_o),
        .ADC_EN1_o(ADC_EN1_o),
        .ADC_EN2_o(ADC_EN2_o),
        .QDAC_o(QDAC_o),
        .RSEL_o(RSEL_o),

        // Col wise signal
        .DUMH_o(DUMH_o),
        .PRECB_o(PRECB_o),
        .DISC_o(DISC_o)
    );

    // Make random data from eFlash PIM
    task automatic random_eFlash1_output();
        // 8 bit * 128
        logic [7:0] choices8b[] = '{
            8'b00000000, 8'b10000000, 8'b11000000, 8'b11100000, 8'b11110000, 8'b11111000, 8'b11111100, 8'b11111110, 8'b11111111
            };
        for (int i = 0; i < 128; i++) begin
            eFlash_output1_i[1023 - 8*i -: 8] = choices8b[$urandom_range(0, choices8b.size()-1)];
        end
        for (int w = 0; w < 32; w++) begin
            logic [31:0] word;
            word = eFlash_output1_i[1023 - 32 * w -: 32];
            $write("%0t  [%02d] 0x%08h  ", $time, w, word);
            if ((w % 4) == 3) $write("\n");
        end
        $write("\n");
    endtask

        // Make random data from eFlash PIM
    task automatic random_eFlash2_output();
        // 8 bit * 128
        logic [7:0] choices8b[] = '{
            8'b00000000, 8'b10000000, 8'b11000000, 8'b11100000, 8'b11110000, 8'b11111000, 8'b11111100, 8'b11111110, 8'b11111111
            };
        for (int i = 0; i < 128; i++) begin
            eFlash_output2_i[1023 - 8*i -: 8] = choices8b[$urandom_range(0, choices8b.size()-1)];
        end
        for (int w = 0; w < 32; w++) begin
            logic [31:0] word;
            word = eFlash_output2_i[1023 - 32 * w -: 32];
            $write("%0t  [%02d] 0x%08h  ", $time, w, word);
            if ((w % 4) == 3) $write("\n");
        end
        $write("\n");
    endtask



    always begin
        #(CLK_PERIOD / 2) i_clk = ~i_clk;
    end

    always @(negedge serial_out) begin
        #(CLK_PERIOD * CLK_FREQ / BAUD_RATE / 2);
        for (int i = 0; i < 8; i++) begin
            #(CLK_PERIOD * CLK_FREQ / BAUD_RATE);
            uart_buffer[uart_buffer_index][i] = serial_out;
        end
        $write("%c", uart_buffer[uart_buffer_index]);
        $fflush();
        uart_buffer_index++;
        if (uart_buffer[uart_buffer_index-1] == 8'h3E)
            response_ready = 1'b1;
        #(CLK_PERIOD * CLK_FREQ / BAUD_RATE);
    end

    // UART send task
    task uart_send;
        input [7:0] data;
        begin
            @(posedge i_clk);
            uart_data_in = data;
            uart_data_in_valid = 1'b1;
            @(posedge i_clk);
            while (!uart_data_in_ready) @(posedge i_clk);
            uart_data_in_valid = 1'b0;
        end
    endtask

    task uart_transfer;
        input [255:0] command;  // packed bit vector
        input [31:0] chars;
        integer i;
        begin
            for (i = 0; i < chars; i++) begin
                if (command[(chars-1-i)*8 +: 8] != 0) begin
                    uart_send(command[(chars-1-i)*8 +: 8]);
                    #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 30);
                end
            end
            uart_send(8'h0D); #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 30);
            uart_send(8'h0A); #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 30);
        end
    endtask


    initial begin
        // Initialize signals
        i_clk = 0;
        i_rv_rst_n = 0;
        i_spi_rst_n = 0;
        spi_start = 0;
        spi_data_in = 0;
        uart_data_in_valid = 1'b0;
        uart_data_out_ready = 1'b0;
        uart_buffer_index = 0;
        response_ready = 0;

        // Reset
		repeat(10) @(posedge i_clk); i_spi_rst_n = 1;  // Hold reset for 40ns (10 clock cycles)

		// ----| PROGRAM FLASH |-------------------------------------------------------------------
		flash_addr = 32'h1000_0000;
		$readmemh("./bios.hex", program_array);
		$display("testbench> start flash program (imem)");
		for (int i = 0; i < 1345; ++i) begin
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
        		spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h02;	// INSTRUCTION DATA
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
			    if (program_array[i] !== 32'hxxxx_xxxx) begin
        		    spi_data_in = program_array[i][(8*j)-1 -: 8];	// SEND ADDRESS BYTES
                end else begin
        		    spi_data_in = '0;	// SEND ADDRESS BYTES
                end
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
			flash_addr = flash_addr + 4;
			$display("testbench> flash addr: %h \t data[%d]: %h", flash_addr, i, program_array[i]);
		end

		flash_addr = 32'h1000_4000;
		$display("testbench> start flash program (dmem)");
		for (int i = 4096; i < 4150; ++i) begin
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
        		spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h02;	// INSTRUCTION DATA
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
			    if (program_array[i] !== 32'hxxxx_xxxx) begin
        		    spi_data_in = program_array[i][(8*j)-1 -: 8];	// SEND ADDRESS BYTES
                end else begin
        		    spi_data_in = '0;	// SEND ADDRESS BYTES
                end
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
			flash_addr = flash_addr + 4;
			$display("testbench> flash addr: %h \t data[%d]: %h", flash_addr, i, program_array[i]);
		end
		$display("testbench> Flash program done\n");

		// ----| SRAM FLASH |-------------------------------------------------------------------
		flash_addr = 32'h2000_0000;
		for (int i = 0; i < 128; ++i) begin
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
        		spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
            @(negedge i_clk);
        	spi_start = 1;
        	spi_data_in = 8'h02;	// INSTRUCTION DATA
        	@(posedge i_clk); #2;
        	spi_start = 0;
        	spi_data_in = 0;
        	@(posedge spi_done);
			for (int j = 4; j > 0; --j) begin
                @(negedge i_clk);
        		spi_start = 1;
			    if (program_array[i] !== 32'hxxxx_xxxx) begin
        		    spi_data_in = $urandom;
                end else begin
        		    spi_data_in = '0;	// SEND ADDRESS BYTES
                end
        	    @(posedge i_clk); #2;
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
			flash_addr = flash_addr + 4;
			$display("testbench> flash addr: %h \t data[%d]: %h", flash_addr, i, spi_data_in);
		end

        random_eFlash1_output();
        random_eFlash2_output();

        #100 i_spi_rst_n = 0; i_rv_rst_n = 1;

        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        //uart_transfer("dump 20000000 10", 17);
        //wait(response_ready); response_ready = 0; uart_buffer_index = 0;

		uart_transfer("pim_erase 4 7 10", 16);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_program 3 11 10 12", 22);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_zp 7897", 11);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_read 20000000 12 9", 24);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_load 20000000 3", 21);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("dump 20000000 1", 17);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_parallel 20000030 10 12", 29);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_load 20000100 1", 21);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("dump 20000100 32", 18);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_rbr 20000088 10 12", 24);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("pim_load 200000ac 2", 21);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;

        uart_transfer("dump 200000ac 32", 18);
        wait(response_ready); response_ready = 0; uart_buffer_index = 0;


        #1000000;
        $finish;
    end

endmodule