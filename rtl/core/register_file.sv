
module register_file #(
    parameter XLEN = 32
) (
    input                       clk_i,
    input                       rst_ni,
    input           [4:0]       rs1_i,
    input           [4:0]       rs2_i,
    input           [4:0]       rd_i,
    input           [XLEN-1:0]  rd_din_i,
    input                       reg_write_i,
    output          [XLEN-1:0]  rs1_dout_o,
    output          [XLEN-1:0]  rs2_dout_o
);

    logic [XLEN-1:0] rf_data[0:31];

    int i;
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            for (i = 0; i < 32; i = i + 1) begin
                rf_data[i] <= '0;
            end
        end else begin
            if (reg_write_i) begin
                if(rd_i == '0) begin
                    rf_data[rd_i] <= '0;            // hard-wired ZERO
                end else begin
                    rf_data[rd_i] <= rd_din_i;
                end
            end else begin
                rf_data[rd_i] <= rf_data[rd_i];
            end
        end
    end

    // output logic for rs1
    assign rs1_dout_o = (reg_write_i && (rs1_i == rd_i)) ? rd_din_i : rf_data[rs1_i];

    // output logic for rs2
    assign rs2_dout_o = (reg_write_i && (rs2_i == rd_i)) ? rd_din_i : rf_data[rs2_i];

endmodule