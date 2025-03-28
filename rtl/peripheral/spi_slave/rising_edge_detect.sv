
module rising_edge_detect (
    input           clk_i,
    input           signal_i,
    output  logic   edge_o
);

    logic prev_signal;

    always_ff @(posedge clk_i) begin
        prev_signal <= signal_i;
        edge_o <= (signal_i && !prev_signal);
    end


endmodule
