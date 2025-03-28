
module program_counter #(
    parameter XLEN = 32,
    parameter RESET_PC = 32'h4000_0000
) (
    input                       clk_i,
    input                       rst_ni,
    input                       pc_write_i,
    input           [XLEN-1:0]  pc_next_i,
    output  logic   [XLEN-1:0]  pc_curr_o
);

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            pc_curr_o <= RESET_PC;
        end else begin
            if (pc_write_i) begin
                pc_curr_o <= pc_next_i;
            end else begin
                pc_curr_o <= pc_curr_o;
            end
        end
    end

endmodule
