module ram_block_imem #(
    parameter IMEM_DEPTH = 4096,
    parameter IMEM_ADDR_WIDTH = 14
) (
    input                       i_clk,
    input [IMEM_ADDR_WIDTH-1:0] i_addr,
    input                       i_we,
    input [3:0]                 i_size,
    input [31:0]                i_din,
    output logic [31:0]         o_dout
);

    localparam DEPTH_WORD = IMEM_DEPTH;

    // Declare BRAM for each byte lane
    (* ram_style = "block" *) logic [7:0] d0 [0:DEPTH_WORD-1];
    (* ram_style = "block" *) logic [7:0] d1 [0:DEPTH_WORD-1];
    (* ram_style = "block" *) logic [7:0] d2 [0:DEPTH_WORD-1];
    (* ram_style = "block" *) logic [7:0] d3 [0:DEPTH_WORD-1];

    initial begin
        $readmemh("imem_0.mem", d0);
        $readmemh("imem_1.mem", d1);
        $readmemh("imem_2.mem", d2);
        $readmemh("imem_3.mem", d3);
    end

    // Base address and next word address
    logic [IMEM_ADDR_WIDTH-3:0] base_addr;
    logic [IMEM_ADDR_WIDTH-3:0] next_addr;

    assign base_addr = i_addr[IMEM_ADDR_WIDTH-1:2];
    assign next_addr = base_addr + 1;

    // Read byte offset
    logic [1:0] byte_offset;

    // Read registers
    logic [7:0] d0_r0, d1_r0, d2_r0, d3_r0;
    logic [7:0] d0_r1, d1_r1, d2_r1, d3_r1;

    always_ff @(posedge i_clk) begin
        d0_r0 <= d0[base_addr];
        d1_r0 <= d1[base_addr];
        d2_r0 <= d2[base_addr];
        d3_r0 <= d3[base_addr];

        d0_r1 <= d0[next_addr];
        d1_r1 <= d1[next_addr];
        d2_r1 <= d2[next_addr];
        d3_r1 <= d3[next_addr];

        byte_offset <= i_addr[1:0];
    end

    // Read mux for unaligned access
    always_comb begin
        case (byte_offset)
            2'b00: o_dout = {d3_r0, d2_r0, d1_r0, d0_r0};
            2'b01: o_dout = {d0_r1, d3_r0, d2_r0, d1_r0};
            2'b10: o_dout = {d1_r1, d0_r1, d3_r0, d2_r0};
            2'b11: o_dout = {d2_r1, d1_r1, d0_r1, d3_r0};
            default: o_dout = 32'hXXXX_XXXX;
        endcase
    end

    // Aligned write only
    always_ff @(posedge i_clk) begin
        if (i_we) begin
            if (i_size[0]) d0[base_addr] <= i_din[7:0];
            if (i_size[1]) d1[base_addr] <= i_din[15:8];
            if (i_size[2]) d2[base_addr] <= i_din[23:16];
            if (i_size[3]) d3[base_addr] <= i_din[31:24];
        end
    end

endmodule
