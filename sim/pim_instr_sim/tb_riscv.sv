
`timescale 1ns/10ps

module mpw_sim;

    parameter CLK_PERIOD = 4;
    parameter CLK_FREQ = 250_000_000;
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
    reg [31:0] program_array [0:2047];
    reg [31:0] flash_addr;

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
        .PIMADDR(),
        .PIMRD({32{1'b1}}),  // Not used in this simulation
        .PIMWD()
    );

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

    task automatic uart_send;
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

    task automatic uart_transfer;
        input [255:0] command;
        input [31:0] chars;
        integer i;
        begin
            for (i = 0; i < chars; i++) begin
                uart_send(command[(chars - 1 - i) * 8 +: 8]);
                #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
            end
            uart_send(8'h0D); #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
            uart_send(8'h0A); #(CLK_PERIOD * CLK_FREQ / BAUD_RATE * 10);
        end
    endtask

    task automatic send_str;
        input string s;
        bit [255:0] command_buf;
        int len;
        begin
            len = s.len();
            command_buf = 0;
            for (int i = 0; i < len; i++) begin
                command_buf |= bit'(s[i]) << (8 * (len - 1 - i));
            end
            uart_transfer(command_buf, len);
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
		$readmemh("./pim_instr.hex", program_array);
		$display("testbench> start flash program");
		for (int i = 0; i < 2048; ++i) begin
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
			    if (program_array[i] !== 32'hxxxx_xxxx) begin
        		    spi_data_in = program_array[i][(8*j)-1 -: 8];	// SEND ADDRESS BYTES
                end else begin
        		    spi_data_in = '0;	// SEND ADDRESS BYTES
                end
        		#3
        		spi_start = 0;
        		spi_data_in = 0;
        		@(posedge spi_done);
			end
			flash_addr = flash_addr + 4;
			$display("testbench> flash addr: %h \t data[%d]: %h", flash_addr, i, program_array[i]);
		end
		$display("testbench> Flash program done\n");
        //----| PIM BUFFER FLASH |-------------------------------------------------------------------
        flash_addr = 32'h2000_0000;
        for (int i = 0; i < 4096; ++i) begin
            #2
                spi_start = 1;
                spi_data_in = 8'h01;    // INSTRUCTION ADDRESS
                #3
                spi_start = 0;
                spi_data_in = 0;
                @(posedge spi_done);
                for (int j = 4; j > 0; --j) begin
                    //$display("%h", flash_addr[(::8*j)-1 -: 8]);
                    #2
                    spi_start = 1;
                    spi_data_in = flash_addr[(8*j)-1 -: 8]; // SEND ADDRESS BYTES
                    #3
                    spi_start = 0;
                    spi_data_in = 0;
                    @(posedge spi_done);
                end
                #2
                spi_start = 1;
                spi_data_in = 8'h02;    // INSTRUCTION DATA
                #3
                spi_start = 0;
                spi_data_in = 0;
                @(posedge spi_done);
                for (int j = 4; j > 0; --j) begin
                    //$display("%h", program_array[i][(8*j)-1 -: 8]);
                    #2
                    spi_start = 1;
                    spi_data_in = $urandom_range(255, 0);   // SEND ADDRESS BYTES
                    #3
                    spi_start = 0;
                    spi_data_in = 0;
                    @(posedge spi_done);
                end
                flash_addr = flash_addr + 4;
        end
        $display("testbench> Flash pim_buffer0 done");


        #100 i_spi_rst_n = 0; i_rv_rst_n = 1;

        repeat(3000000) @(posedge i_clk); i_rv_rst_n = 0;
        $finish;
    end

endmodule
