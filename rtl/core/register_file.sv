
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
    output logic    [XLEN-1:0]  rs1_dout_o,
    output logic    [XLEN-1:0]  rs2_dout_o
);

    logic [XLEN-1:0] rf_data_debug_0;
    logic [XLEN-1:0] rf_data_debug_1;
    logic [XLEN-1:0] rf_data_debug_2;
    logic [XLEN-1:0] rf_data_debug_3;
    logic [XLEN-1:0] rf_data_debug_4;
    logic [XLEN-1:0] rf_data_debug_5;
    logic [XLEN-1:0] rf_data_debug_6;
    logic [XLEN-1:0] rf_data_debug_7;
    logic [XLEN-1:0] rf_data_debug_8;
    logic [XLEN-1:0] rf_data_debug_9;
    logic [XLEN-1:0] rf_data_debug_10;
    logic [XLEN-1:0] rf_data_debug_11;
    logic [XLEN-1:0] rf_data_debug_12;
    logic [XLEN-1:0] rf_data_debug_13;
    logic [XLEN-1:0] rf_data_debug_14;
    logic [XLEN-1:0] rf_data_debug_15;
    logic [XLEN-1:0] rf_data_debug_16;
    logic [XLEN-1:0] rf_data_debug_17;
    logic [XLEN-1:0] rf_data_debug_18;
    logic [XLEN-1:0] rf_data_debug_19;
    logic [XLEN-1:0] rf_data_debug_20;
    logic [XLEN-1:0] rf_data_debug_21;
    logic [XLEN-1:0] rf_data_debug_22;
    logic [XLEN-1:0] rf_data_debug_23;
    logic [XLEN-1:0] rf_data_debug_24;
    logic [XLEN-1:0] rf_data_debug_25;
    logic [XLEN-1:0] rf_data_debug_26;
    logic [XLEN-1:0] rf_data_debug_27;
    logic [XLEN-1:0] rf_data_debug_28;
    logic [XLEN-1:0] rf_data_debug_29;
    logic [XLEN-1:0] rf_data_debug_30;
    logic [XLEN-1:0] rf_data_debug_31;
    
    
    always_comb begin
        rf_data_debug_0 = rf_data[0];
        rf_data_debug_1 = rf_data[1];
        rf_data_debug_2 = rf_data[2];
        rf_data_debug_3 = rf_data[3];
        rf_data_debug_4 = rf_data[4];
        rf_data_debug_5 = rf_data[5];
        rf_data_debug_6 = rf_data[6];
        rf_data_debug_7 = rf_data[7];
        rf_data_debug_8 = rf_data[8];
        rf_data_debug_9 = rf_data[9];
        rf_data_debug_10 = rf_data[10];
        rf_data_debug_11 = rf_data[11];
        rf_data_debug_12 = rf_data[12];
        rf_data_debug_13 = rf_data[13];
        rf_data_debug_14 = rf_data[14];
        rf_data_debug_15 = rf_data[15];
        rf_data_debug_16 = rf_data[16];
        rf_data_debug_17 = rf_data[17];
        rf_data_debug_18 = rf_data[18];
        rf_data_debug_19 = rf_data[19];
        rf_data_debug_20 = rf_data[20];
        rf_data_debug_21 = rf_data[21];
        rf_data_debug_22 = rf_data[22];
        rf_data_debug_23 = rf_data[23];
        rf_data_debug_24 = rf_data[24];
        rf_data_debug_25 = rf_data[25];
        rf_data_debug_26 = rf_data[26];
        rf_data_debug_27 = rf_data[27];
        rf_data_debug_28 = rf_data[28];
        rf_data_debug_29 = rf_data[29];
        rf_data_debug_30 = rf_data[30];
        rf_data_debug_31 = rf_data[31];
    end

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
    always_comb begin
        if (rs1_i == '0) begin
            rs1_dout_o = '0;
        end else begin
            if (reg_write_i && (rs1_i == rd_i)) begin
                rs1_dout_o = rd_din_i;
            end else begin
                rs1_dout_o = rf_data[rs1_i];
            end
        end
    end

    // output logic for rs2
    always_comb begin
        if (rs2_i == '0) begin
            rs2_dout_o = '0;
        end else begin
            if (reg_write_i && (rs2_i == rd_i)) begin
                rs2_dout_o = rd_din_i;
            end else begin
                rs2_dout_o = rf_data[rs2_i];
            end
        end
    end

endmodule