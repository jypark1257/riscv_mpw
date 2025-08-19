`timescale 1ns/10ps

module mpw_sim;
    // Parameters
    parameter CLK_PERIOD = 4;  // 4ns clock period
    parameter CLK_FREQ = 250000000;
    parameter BAUD_RATE = 115200;
    parameter SPI_CLK_FREQ = 1000000;

    // Signals
    reg i_clk;
    reg i_rv_rst_n;
    reg i_spi_rst_n;
	reg o_sync_rst_n;
    // UART Signals
    reg [7:0] uart_data_in;
    reg uart_data_in_valid;
    wire uart_data_in_ready;
    wire [7:0] uart_data_out;
    wire uart_data_out_valid;
    reg uart_data_out_ready;
    wire serial_in;
    wire serial_out;

    // SPI Signals
    wire sclk;
    wire mosi;
    wire miso;
    wire cs;
    reg spi_start;
    wire spi_done;
    reg [7:0] spi_data_in;
    reg [31:0] program_array [0:(4096 *2)-1];
    reg [31:0] flash_addr;

    // UART buffer
    reg [7:0] uart_buffer [2048:0];
    integer uart_buffer_index;
    reg response_ready;

	// sync reset
	logic sync_rst_n;

	// string to be transfer
	string str;

	// cycle counter
	reg [31:0] cycle;

    // Instance the UART 
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

    // Instance the SPI MASTER 
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

    // Instantiate the DUT (Design Under Test)
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
        .SYNCRSTN(o_sync_rst_n)
    );


     // Clock generation
    always begin
        #(CLK_PERIOD/2) i_clk = ~i_clk;
    end

    // UART receive task
    always @(negedge serial_out) begin
        #(CLK_PERIOD * CLK_FREQ / BAUD_RATE / 2);
        
        for (int i = 0; i < 8; i = i + 1) begin
            #(CLK_PERIOD * CLK_FREQ / BAUD_RATE);
            uart_buffer[uart_buffer_index][i] = serial_out;
        end
        
        $write("%c", uart_buffer[uart_buffer_index]);
        $fflush();
        
        uart_buffer_index = uart_buffer_index + 1;
        
        if (uart_buffer[uart_buffer_index-1] == 8'h3E) begin // '>' character
            response_ready = 1'b1;
        end
        
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
		input [255:0] command;
		input [31:0] chars;
		integer i;
		begin
			for (i = 0; i < chars; i = i + 1) begin
				if (command[(chars-1-i)*8 +: 8] != 0) begin
					uart_send(command[(chars-1-i)*8 +: 8]);
					#(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
				end
			end
			// send newline
			uart_send(8'h0D);
			#(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
			uart_send(8'h0A);
			#(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
		end
	endtask

    // Test stimulus
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
		for (int i = 0; i < 4200; ++i) begin
			if (program_array[i] !== 32'hxxxx_xxxx) begin
				//$display("%h", program_array[i]);
				#2
        	    spi_start = 1;
        	    spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        	    #3
        	    spi_start = 0;
        	    spi_data_in = 0;
        	    @(posedge spi_done);
				for (int j = 4; j > 0; --j) begin
					//$display("%h", flash_addr[(8*j)-1 -: 8]);
					#2
        	    	spi_start = 1;
        	    	spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        	    	#3
        	    	spi_start = 0;
        	    	spi_data_in = 0;
        	    	@(posedge spi_done);
				end
				#2
        	    spi_start = 1;
        	    spi_data_in = 8'h02;	// INSTRUCTION DATA
        	    #3
        	    spi_start = 0;
        	    spi_data_in = 0;
        	    @(posedge spi_done);
				for (int j = 4; j > 0; --j) begin
					//$display("%h", program_array[i][(8*j)-1 -: 8]);
					#2
        	    	spi_start = 1;
        	    	spi_data_in = program_array[i][(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        	    	#3
        	    	spi_start = 0;
        	    	spi_data_in = 0;
        	    	@(posedge spi_done);
				end
				flash_addr = flash_addr + 4;
			end
		end
		$display("testbench> Flash program done\n");

		//// ----| PIM BUFFER FLASH |-------------------------------------------------------------------
		//flash_addr = 32'h2000_0000;
		//for (int i = 0; i < 4096; ++i) begin
		//    #2
        //	    spi_start = 1;
        //	    spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        //	    #3
        //	    spi_start = 0;
        //	    spi_data_in = 0;
        //	    @(posedge spi_done);
		//		for (int j = 4; j > 0; --j) begin
		//			//$display("%h", flash_addr[(::8*j)-1 -: 8]);
		//			#2
        //	    	spi_start = 1;
        //	    	spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        //	    	#3
        //	    	spi_start = 0;
        //	    	spi_data_in = 0;
        //	    	@(posedge spi_done);
		//		end
		//		#2
        //	    spi_start = 1;
        //	    spi_data_in = 8'h02;	// INSTRUCTION DATA
        //	    #3
        //	    spi_start = 0;
        //	    spi_data_in = 0;
        //	    @(posedge spi_done);
		//		for (int j = 4; j > 0; --j) begin
		//			//$display("%h", program_array[i][(8*j)-1 -: 8]);
		//			#2
        //	    	spi_start = 1;
        //	    	spi_data_in = $urandom_range(255, 0);	// SEND ADDRESS BYTES
        //	    	#3
        //	    	spi_start = 0;
        //	    	spi_data_in = 0;
        //	    	@(posedge spi_done);
		//		end
		//		flash_addr = flash_addr + 4;
		//end
		//$display("testbench> Flash pim_buffer0 done");
		//flash_addr = 32'h2000_4000;
		//for (int i = 0; i < 4096; ++i) begin
		//    #2
        //	    spi_start = 1;
        //	    spi_data_in = 8'h01;	// INSTRUCTION ADDRESS
        //	    #3
        //	    spi_start = 0;
        //	    spi_data_in = 0;
        //	    @(posedge spi_done);
		//		for (int j = 4; j > 0; --j) begin
		//			//$display("%h", flash_addr[(::8*j)-1 -: 8]);
		//			#2
        //	    	spi_start = 1;
        //	    	spi_data_in = flash_addr[(8*j)-1 -: 8];	// SEND ADDRESS BYTES
        //	    	#3
        //	    	spi_start = 0;
        //	    	spi_data_in = 0;
        //	    	@(posedge spi_done);
		//		end
		//		#2
        //	    spi_start = 1;
        //	    spi_data_in = 8'h02;	// INSTRUCTION DATA
        //	    #3
        //	    spi_start = 0;
        //	    spi_data_in = 0;
        //	    @(posedge spi_done);
		//		for (int j = 4; j > 0; --j) begin
		//			//$display("%h", program_array[i][(8*j)-1 -: 8]);
		//			#2
        //	    	spi_start = 1;
        //	    	spi_data_in = $urandom_range(255, 0);	// SEND ADDRESS BYTES
        //	    	#3
        //	    	spi_start = 0;
        //	    	spi_data_in = 0;
        //	    	@(posedge spi_done);
		//		end
		//		flash_addr = flash_addr + 4;
		//end
		//$display("testbench> Flash pim_buffer1 done");

        #100 i_spi_rst_n = 0; i_rv_rst_n = 1;


        // Wait for initial prompt
        wait(response_ready);
        response_ready = 0;
        uart_buffer_index = 0;	

		// Send command: help
		str = "help";
		uart_transfer(str, str.len());

		// Wait for response
		wait(response_ready);
		response_ready = 0;
		uart_buffer_index = 0;


        #1000000; // Run for a bit longer
        $finish;
    end

endmodule

