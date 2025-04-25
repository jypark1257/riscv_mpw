
module uart_wrap_test #(
    parameter CLOCK_FREQ            = 125_000_000,
    parameter BAUD_RATE             = 115_200,
    parameter UART_CTRL             = 32'h8000_0000,
    parameter UART_RECV             = 32'h8000_0004,
    parameter UART_TRANS            = 32'h8000_0008,
    parameter UART_SYMBOL_EDGE_TIME = 32'h8000_000C,
    parameter UART_SAMPLE_TIME      = 32'h8000_0010

) (
    input                   clk_i, 
    input                   rst_ni, 

    input           [31:0]  uart_addr_i,
    input                   uart_write_i,
    input                   uart_read_i,
    input           [ 3:0]  uart_size_i,
    input           [31:0]  uart_din_i,
    output logic    [31:0]  uart_dout_o,

    // serial IO
    input                   serial_rx_i,
    output logic            serial_tx_o
);

    logic [15:0] symbol_edge_time;
    logic [15:0] sample_time;

    logic [31:0] uart_addr;
    logic uart_read;

    // inputs
    logic [7:0] data_in;
    logic data_in_valid;
    logic data_out_ready;

    // outputs
    logic [7:0] data_out;
    logic data_in_ready;
    logic data_out_valid;

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            uart_addr <= '0;
            uart_read <= '0;
        end else begin
            uart_addr <= uart_addr_i;
            uart_read <= uart_read_i;
        end
    end

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            symbol_edge_time <= '0;
            sample_time <= '0;
        end else begin
            symbol_edge_time    <= ((uart_addr_i == UART_SYMBOL_EDGE_TIME) && (uart_write_i)) ? uart_din_i[15:0] : symbol_edge_time;
            sample_time         <= ((uart_addr_i == UART_SAMPLE_TIME) && (uart_write_i)) ? uart_din_i[15:0] : sample_time;
        end
    end

    // assign inputs
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            data_in <= '0;
            data_in_valid <= '0;
            data_out_ready <= '0;
        end else begin
            data_in <= ((uart_addr_i == UART_TRANS) && (uart_write_i)) ? uart_din_i[7:0] : data_in;
            data_in_valid <= ((uart_addr_i == UART_TRANS) && (uart_write_i));
            data_out_ready <= ((uart_addr_i == UART_RECV) && (uart_read_i));
        end
    end

    always_comb begin
        if (uart_read == '0) begin
            uart_dout_o = '0;
        end else begin
            case (uart_addr)
                UART_CTRL: begin    
                    uart_dout_o = {30'b0, data_out_valid, data_in_ready};
                end
                UART_RECV: begin
                    uart_dout_o = {24'b0, data_out};
                end
                default: begin
                    uart_dout_o = '0;
                end
            endcase
        end
    end

    //UART
    uart #(
        .CLOCK_FREQ(CLOCK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) on_chip_uart (
        .clk            (clk_i),
        .reset          (!rst_ni),

        //.symbol_edge_time(symbol_edge_time),
        //.sample_time(sample_time),

        .data_in        (data_in),
        .data_in_valid  (data_in_valid),
        .data_out_ready (data_out_ready),
        .serial_in      (serial_rx_i),

        .data_in_ready  (data_in_ready),
        .data_out       (data_out),
        .data_out_valid (data_out_valid),
        .serial_out     (serial_tx_o)
    );

endmodule


module uart_test #(
    parameter CLOCK_FREQ = 125_000_000,
    parameter BAUD_RATE = 115_200)
(
    input clk,
    input reset,

    input [15:0] symbol_edge_time,
    input [15:0] sample_time,

    input [7:0] data_in,
    input data_in_valid,
    output data_in_ready,

    output [7:0] data_out,
    output data_out_valid,
    input data_out_ready,

    input serial_in,
    output serial_out
);
    reg serial_in_reg, serial_out_reg;
    wire serial_out_tx;
    assign serial_out = serial_out_reg;
    always @ (posedge clk) begin
        serial_out_reg <= reset ? 1'b1 : serial_out_tx;
        serial_in_reg <= reset ? 1'b1 : serial_in;
    end

    uart_transmitter_test #(
        .CLOCK_FREQ(CLOCK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) uatransmit (
        .clk(clk),
        .reset(reset),
        .symbol_edge_time(symbol_edge_time),
        .data_in(data_in),
        .data_in_valid(data_in_valid),
        .data_in_ready(data_in_ready),
        .serial_out(serial_out_tx)
    );

    uart_receiver_test #(
        .CLOCK_FREQ(CLOCK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) uareceive (
        .clk(clk),
        .reset(reset),
        .symbol_edge_time(symbol_edge_time),
        .sample_time(sample_time),
        .data_out(data_out),
        .data_out_valid(data_out_valid),
        .data_out_ready(data_out_ready),
        .serial_in(serial_in_reg)
    );
endmodule


module uart_receiver_test #(
    parameter CLOCK_FREQ = 125_000_000,
    parameter BAUD_RATE = 115_200)
(
    input clk,
    input reset,

    input [15:0] symbol_edge_time,
    input [15:0] sample_time,

    output [7:0] data_out,
    output data_out_valid,
    input data_out_ready,

    input serial_in
);

    wire symbol_edge;
    wire sample;
    wire start;
    wire rx_running;

    reg [9:0] rx_shift;
    reg [3:0] bit_counter;
    reg [15:0] clock_counter;
    reg has_byte;

    //--|Signal Assignments|------------------------------------------------------

    // Goes high at every symbol edge
    /* verilator lint_off WIDTH */
    assign symbol_edge = clock_counter == (symbol_edge_time - 1);
    /* lint_on */

    // Goes high halfway through each symbol
    /* verilator lint_off WIDTH */
    assign sample = clock_counter == sample_time;
    /* lint_on */

    // Goes high when it is time to start receiving a new character
    assign start = !serial_in && !rx_running;

    // Goes high while we are receiving a character
    assign rx_running = bit_counter != 4'd0;

    // Outputs
    assign data_out = rx_shift[8:1];
    assign data_out_valid = has_byte && !rx_running;

    //--|Counters|----------------------------------------------------------------

    // Counts cycles until a single symbol is done
    always @ (posedge clk) begin
        clock_counter <= (start || reset || symbol_edge) ? 0 : clock_counter + 1;
    end

    // Counts down from 10 bits for every character
    always @ (posedge clk) begin
        if (reset) begin
            bit_counter <= 0;
        end else if (start) begin
            bit_counter <= 10;
        end else if (symbol_edge && rx_running) begin
            bit_counter <= bit_counter - 1;
        end
    end

    //--|Shift Register|----------------------------------------------------------
    always @(posedge clk) begin
        if (sample && rx_running) rx_shift <= {serial_in, rx_shift[9:1]};
    end

    //--|Extra State For Ready/Valid|---------------------------------------------
    // This block and the has_byte signal aren't needed in the uart_transmitter
    always @ (posedge clk) begin
        if (reset) has_byte <= 1'b0;
        else if (bit_counter == 1 && symbol_edge) has_byte <= 1'b1;
        else if (data_out_ready) has_byte <= 1'b0;
    end
endmodule

module uart_transmitter_test #(
    parameter CLOCK_FREQ = 125_000_000,
    parameter BAUD_RATE = 115_200)
(
    input clk,
    input reset,

    input [15:0] symbol_edge_time,

    input [7:0] data_in,
    input data_in_valid,
    output data_in_ready,

    output serial_out
);

    // See diagram in the lab guide
    
    //integer symbol_edge_time = SYMBOL_EDGE_TIME;
    //integer clock_counter_width = CLOCK_COUNTER_WIDTH;

    wire symbol_edge, start;
    // Remove these assignments when implementing this module
    reg [9:0] data_shift;

    // counters
    reg [3:0] bit_counter;
    reg [15:0] clock_counter;

    // outputs
    assign data_in_ready = bit_counter == 0;
    assign serial_out = (!data_in_ready) ? data_shift[0] : 1'b1; 

    //goes high when symbol edge detected
    /* verilator lint_off WIDTH*/	
    assign symbol_edge = clock_counter == (symbol_edge_time - 1);
    //assign start = bit_counter == FULL_DATA_COUNT;

    //goes high when ready to record data_in and trigger transmission 
    assign start = data_in_ready && data_in_valid;

    always @(posedge clk) begin
	    //keep track of past cycles before SYMBOL_EDGE_TIME
	    clock_counter <= (reset || start || symbol_edge) ? 0 : clock_counter + 1;
        //record LSB of data to be output on serial line

	    if (reset) begin
            bit_counter <= 0;
            data_shift <= 9'd0; //prevent undefined values
        end

	    //if transmitting in progress and symbol edge time constraint met
        else if (!data_in_ready && symbol_edge) begin
	        data_shift <= data_shift >> 1; //output next bit
	       bit_counter <= bit_counter - 4'd1;    //decrement counter 
	    end 
	    //record data_in and trigger transmission
	    else if (start) begin
	        data_shift <= {1'b1, data_in, 1'b0};//include start & stop bit in data to be shifted out
	        bit_counter <= 4'd10;       //initialize
	    end 
    end

endmodule