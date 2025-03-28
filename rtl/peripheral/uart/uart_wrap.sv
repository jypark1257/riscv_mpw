
module uart_wrap #(
    parameter CLOCK_FREQ    = 125_000_000,
    parameter BAUD_RATE     = 115_200,
    parameter UART_CTRL     = 32'h8000_0000,
    parameter UART_RECV     = 32'h8000_0004,
    parameter UART_TRANS    = 32'h8000_0008
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

        .data_in        (data_in),
        .data_in_valid  (data_in_valid),
        .data_out_ready (data_out_ready),
        .serial_in      (i_serial_rx),

        .data_in_ready  (data_in_ready),
        .data_out       (data_out),
        .data_out_valid (data_out_valid),
        .serial_out     (serial_tx_o)
    );

endmodule