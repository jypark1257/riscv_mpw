module fifo_unit #(
    parameter           ENTRY = 4,
    parameter           XLEN = 32,
    parameter           RESET_PC = 32'h1000_0000
) (
    input logic                 clk_i,
    input logic                 rst_ni,

    // input port 
    input logic [XLEN-1:0]      in_addr_i,
    input logic [XLEN-1:0]      in_instr_i,
    input logic                 in_valid_i,

    // control signal
    input logic                 clear_i,
    output logic                fetch_ready_o,          //request the fetch

    // output port
    output logic [XLEN-1:0]      out_addr_o,
    output logic [XLEN-1:0]      out_instr_o
);
    logic [XLEN-1:0]        instr_q_0;
    logic [XLEN-1:0]        instr_q_1;
    logic [XLEN-1:0]        instr_q_2;
    logic [XLEN-1:0]        instr_q_3;

    assign instr_q_0 = instr_q[0];
    assign instr_q_1 = instr_q[1];
    assign instr_q_2 = instr_q[2];
    assign instr_q_3 = instr_q[3];
    logic [XLEN-1:0]        instr_d_0;
    logic [XLEN-1:0]        instr_d_1;
    logic [XLEN-1:0]        instr_d_2;
    logic [XLEN-1:0]        instr_d_3;

    assign instr_d_0 = instr_d[0];
    assign instr_d_1 = instr_d[1];
    assign instr_d_2 = instr_d[2];
    assign instr_d_3 = instr_d[3];


    logic [XLEN-1:0]        instr_d[ENTRY-1:0];
    logic [XLEN-1:0]        instr_q[ENTRY-1:0];

    logic [XLEN-1:0]        addr_d[ENTRY-1:0];
    logic [XLEN-1:0]        addr_q[ENTRY-1:0];


    logic        valid_d[ENTRY-1:0];  
    logic        valid_q[ENTRY-1:0];

    logic [XLEN-1:0]        instr, instr_unaligned;

    logic           aligned_is_compressed, unaligned_is_compressed;

    // check the compression
    assign aligned_is_compressed = instr_q[0][1:0] != 2'b11;
    assign unaligned_is_compressed = instr_q[0][17:16] != 2'b11;

    assign instr_unaligned = (valid_q[1]) ? {instr_q[1][15:0], instr_q[0][31:16]} : {in_instr_i[15:0], instr_q[0][31:16]};

    assign out_addr_o = addr_q[0];

    // output port _ instruction
    logic check_aligned;
    assign check_aligned = addr_q[0][1];
    always_comb begin
        if (check_aligned) begin
            out_instr_o = instr_unaligned;
        end else begin
            out_instr_o = instr_q[0];
        end
    end

    // fetch request
    assign fetch_ready_o = ~valid_q[ENTRY-2];

    ////////////////
    // FIFO entry //
    ////////////////

    // lowest free entry

    logic [ENTRY-1:0]  lowest_free_entry;

    always_comb begin
        for (int i = 0; i < ENTRY; i++) begin
            if (i == 0) begin
                lowest_free_entry[i] = ~valid_q[i];
            end else begin
                lowest_free_entry[i] = ~valid_q[i] & valid_q[i-1];
            end
        end
    end

    // register
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (!rst_ni) begin
            for (int i = 0; i < (ENTRY); i++) begin
                instr_q[i] <= '0;
                addr_q[i] <= '0;
                valid_q[i] <= '0;
            end
        end else begin
            for (int i = 0; i < (ENTRY); i++) begin
                instr_q[i] <= instr_d[i];
                addr_q[i] <= addr_d[i];
                valid_q[i] <= valid_d[i];
            end
        end
    end


    //////////////////////////////////////////
    // output instruction's current address // 
    //////////////////////////////////////////

    logic [XLEN-1:0] addr_next_entry;

    assign addr_next_entry = {addr_q[0][31:2], 2'b00} + 32'h4;

    // output port _ address
    always_comb begin
        for (int i = 0; i < ENTRY; ++i) begin
            instr_d[i] = '0;
            valid_d[i] = '0;
            addr_d[i] = '0;
        end
        if (clear_i) begin
            for (int i = 0; i < ENTRY; i++) begin
                addr_d[i] = '0;
                instr_d[i] = '0;
                valid_d[i] = '0;
            end 
        end else begin
            if (in_valid_i) begin
                if (lowest_free_entry[0]) begin
                    instr_d[0] = in_instr_i;
                    addr_d[0] = in_addr_i;
                    valid_d[0] = 1'b1;
                end else if (lowest_free_entry[1]) begin
                    instr_d[0] = instr_q[0];
                    addr_d[0] = addr_q[0];
                    valid_d[0] = valid_q[0];
                    instr_d[1] = in_instr_i;
                    addr_d[1] = in_addr_i;
                    valid_d[1] = 1'b1;
                end else if (lowest_free_entry[2]) begin
                    instr_d[0] = instr_q[0];
                    addr_d[0] = addr_q[0];
                    valid_d[0] = valid_q[0];
                    instr_d[1] = instr_q[1];
                    addr_d[1] = addr_q[1];
                    valid_d[1] = valid_q[1];
                    instr_d[2] = in_instr_i;
                    addr_d[2] = in_addr_i;
                    valid_d[2] = 1'b1;
                end else if (lowest_free_entry[3]) begin
                    instr_d[0] = instr_q[0];
                    addr_d[0] = addr_q[0];
                    valid_d[0] = valid_q[0];
                    instr_d[1] = instr_q[1];
                    addr_d[1] = addr_q[1];
                    valid_d[1] = valid_q[1];
                    instr_d[2] = instr_q[2];
                    addr_d[2] = addr_q[2];
                    valid_d[2] = valid_q[2];
                    instr_d[3] = in_instr_i;
                    addr_d[3] = in_addr_i;
                    valid_d[3] = 1'b1;
                end else begin
                    instr_d[0] = instr_q[0];
                    addr_d[0] = addr_q[0];
                    valid_d[0] = valid_q[0];
                    instr_d[1] = instr_q[1];
                    addr_d[1] = addr_q[1];
                    valid_d[1] = valid_q[1];
                    instr_d[2] = instr_q[2];
                    addr_d[2] = addr_q[2];
                    valid_d[2] = valid_q[2];
                    instr_d[3] = instr_q[3];
                    addr_d[3] = addr_q[3];
                    valid_d[3] = valid_q[3];
                end
            end
            //if (addr_q[0][1]) begin            // unaligned
            //    for (int i = 0; i < (ENTRY-1); i++) begin
            //        instr_d[i] = instr_q[i+1];
            //        valid_d[i] = valid_q[i+1];
            //    end
            //    for (int j = 1; j < (ENTRY-1); j++) begin
            //        addr_d[j] = addr_q[j+1];
            //    end
            //    instr_d[ENTRY-1] = 32'b0;
            //    valid_d[ENTRY-1] = 1'b0;
            //    addr_d[ENTRY-1] = 32'b0;
            //    if (unaligned_is_compressed) begin
            //        addr_d[0] = addr_next_entry;
            //    end else begin
            //        addr_d[0] = {addr_next_entry[31:2], 2'b10};
            //    end
            //end else begin                      // aligned
            //    if (aligned_is_compressed) begin
            //        for (int i = 0; i < ENTRY; i++) begin
            //            instr_d[i] = instr_q[i];
            //            valid_d[i] = valid_q[i];
            //        end
            //        for (int j = 1; j < ENTRY; j++) begin
            //            addr_d[j] = addr_q[j];
            //        end
            //        addr_d[0] = {addr_q[0][31:2], 2'b10};
            //    end else begin
            //        for (int i = 0; i < (ENTRY-1); i++) begin
            //            instr_d[i] = instr_q[i+1];
            //            valid_d[i] = valid_q[i+1];
            //        end
            //        instr_d[ENTRY-1] = 32'b0;
            //        valid_d[ENTRY-1] = 1'b0;
            //        for (int j = 1; j < (ENTRY-1); j++) begin
            //        addr_d[j] = addr_q[j+1];
            //        end
            //        addr_d[ENTRY-1] = 32'b0;
            //        addr_d[0] = addr_next_entry;
            //    end
            //end
        end
    end


    

endmodule
