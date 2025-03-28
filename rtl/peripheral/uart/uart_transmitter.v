module uart_transmitter #(
    parameter CLOCK_FREQ = 125_000_000,
    parameter BAUD_RATE = 115_200)
(
    input clk,
    input reset,

    input [7:0] data_in,
    input data_in_valid,
    output data_in_ready,

    output serial_out
);

    // See diagram in the lab guide
    localparam  SYMBOL_EDGE_TIME    =   CLOCK_FREQ / BAUD_RATE;
    localparam  CLOCK_COUNTER_WIDTH =   $clog2(SYMBOL_EDGE_TIME);
    
    //integer sumbol_edge_time = SYMBOL_EDGE_TIME;
    //integer clock_counter_width = CLOCK_COUNTER_WIDTH;

    wire symbol_edge, start;
    // Remove these assignments when implementing this module
    reg [9:0] data_shift;

    // counters
    reg [3:0] bit_counter;
    reg [CLOCK_COUNTER_WIDTH-1:0] clock_counter;

    // outputs
    assign data_in_ready = bit_counter == 0;
    assign serial_out = (!data_in_ready) ? data_shift[0] : 1'b1; 

    //goes high when symbol edge detected
    /* verilator lint_off WIDTH*/	
    assign symbol_edge = clock_counter == (SYMBOL_EDGE_TIME - 1);
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