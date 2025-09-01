`timescale 1ns / 1ps
module fpga_top(
    input sysclk_n,
    input sysclk_p,
    input rst_ni,
    input spi_rst_ni,

    // SPI
    input i_sclk,
    input i_cs,
    input i_mosi,
    output o_miso,

    // LEDs
    output reg rst_led,
    output reg spi_rst_led,
    output reg sclk_led,
    output reg cs_led,
    output reg mosi_led,
    output reg miso_led,
    output reg tx_led, 
    output reg rx_led,
    
    // UART TX/RX 
    input i_serial_rx,
    output o_serial_tx
    );    

    // Clock wires
    wire clk_in_bufg;
    wire clkfb_out;
    wire clkfb_buf;
    wire clk_mmcm_out;
    wire sysclk;


    // ─── Internal SPI/UART wires ───────────────────────────
    wire cpu_tx, cpu_rx;
    wire sclk, cs, mosi, miso;

    // clock wiazard
    clk_wiz_0 u_clk_wiz (
        .clk_out1(sysclk),
        .clk_in1_p(sysclk_p),
        .clk_in1_n(sysclk_n)
    );

    // ─── SPI IOB ───────────────────────────────────────────
    (* IOB = "true" *) reg fpga_sclk_iob;
    (* IOB = "true" *) reg fpga_cs_iob;
    (* IOB = "true" *) reg fpga_mosi_iob;
    (* IOB = "true" *) reg fpga_miso_iob;

    // ─── UART IOB ──────────────────────────────────────────
    (* IOB = "true" *) reg fpga_serial_tx_iob;
    (* IOB = "true" *) reg fpga_serial_rx_iob;

    // ─── LED Control ───────────────────────────────────────
    always @(posedge sysclk or negedge spi_rst_ni) begin
        if (~spi_rst_ni) begin
            spi_rst_led <= 1'b0;
            sclk_led <= 1'b0;
            cs_led <= 1'b0;
            mosi_led <= 1'b0;
            miso_led <= 1'b0;
        end else begin
            spi_rst_led <= 1'b1;
            sclk_led <= fpga_sclk_iob;
            cs_led <= fpga_cs_iob;
            mosi_led <= fpga_mosi_iob;
            miso_led <= fpga_miso_iob;
        end
    end

    always @(posedge sysclk or negedge rst_ni) begin
        if (~rst_ni) begin
            rst_led <= 1'b0;
            tx_led <= 1'b0;
            rx_led <= 1'b0;
        end else begin
            rst_led <= 1'b1;
            tx_led <= ~fpga_serial_tx_iob;
            rx_led <= ~fpga_serial_rx_iob;
        end
    end

    // ─── Core logic ────────────────────────────────────────
    mpw_top #(
        .FPGA(1)
    ) u_core_top_0 (
        .CLK(sysclk),
        .RVRSTN(rst_ni),
        .SPIRSTN(spi_rst_ni),
        // SPI
        .SCLK(sclk),
        .CS(cs),
        .MOSI(mosi),
        .MISO(miso),

        .SERIALRX(cpu_rx),
        .SERIALTX(cpu_tx),

        .PIMADDR(),
        .PIMWD(),
        .PIMRD()
    );

    // ─── SPI IOB logic ─────────────────────────────────────
    assign o_miso = fpga_miso_iob;
    assign sclk = fpga_sclk_iob;
    assign cs = fpga_cs_iob;
    assign mosi = fpga_mosi_iob;
    always @(posedge sysclk) begin
        fpga_miso_iob <= miso;
        fpga_sclk_iob <= i_sclk;
        fpga_cs_iob <= i_cs;
        fpga_mosi_iob <= i_mosi;
    end

    // ─── UART IOB logic ────────────────────────────────────
    assign o_serial_tx = fpga_serial_tx_iob;
    assign cpu_rx = fpga_serial_rx_iob;
    always @(posedge sysclk) begin
        fpga_serial_tx_iob <= cpu_tx;
        fpga_serial_rx_iob <= i_serial_rx;
    end

endmodule
