
module spi_slave(
    input                   clk_i,
    input                   rst_ni,
    input                   sclk_i,
    input                   ss_ni,
    input                   mosi_i,
    output                  miso_o,
    input           [31:0]  data_i,
    output  logic   [31:0]  data_o
);

    logic [31:0] RBUF, TBUF;
    logic [31:0] r_dat;
    logic d_ssn;
    logic w_rstn;

    assign miso_o = TBUF[31];

    always_ff @(posedge sclk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            RBUF <= 32'h00;
        end else begin
            RBUF <= {RBUF[30:00], mosi_i};
        end
    end

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            d_ssn <= 1'b1;
        end else begin
            d_ssn <= ss_ni;
        end
    end

    assign w_rstn = ((ss_ni == 1'b0) && (d_ssn == 1'b1)) ? 1'b0 : 1'b1;

    always_ff @(negedge sclk_i or negedge w_rstn) begin
        if (w_rstn == 1'b0) begin
            TBUF <= r_dat;
        end else begin
            TBUF <= {TBUF[30:00], 1'b0};
        end
    end

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            r_dat <= 32'h00;
            data_o <= 32'h00;
        end else begin
            if (ss_ni == 1'b1) begin
                  r_dat <= data_i;
                  data_o <= RBUF;
            end
        end
    end

endmodule
