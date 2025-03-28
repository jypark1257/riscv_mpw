/*
    CS must released and reactivated between blocks (1 byte),
    Use "write_byte" function in spidev
*/

module spi_slave_wrap (
    // SYSTEM CLOCK
    input                   clk_i,
    input                   rst_ni,
    // BUS INTERFACE
    output logic            req_spi_o,
    input                   gnt_spi_i,
    output logic    [31:0]  spi_addr_o,
    input           [31:0]  spi_rd_data_i,
    output logic    [31:0]  spi_wr_data_o,
    output logic    [ 3:0]  spi_size_o,
    output logic            spi_read_o,
    output logic            spi_write_o,
    // SPI SLAVE INTERFACE
    input                   sclk_i,
    input                   cs_i,
    input                   mosi_i,
    output logic            miso_o
);

    // Commands
    localparam ADDR_MODE    = 8'h1;
    localparam DATA_MODE    = 8'h2;

    // FSM states
    typedef enum logic [2:0] { IDLE, WAIT_CMD, READ_ADDR, READ_DATA, BUS_WRITE } e_states;
    
    // state registers
    e_states curr_state;
    e_states next_state;

    // buffers
    logic [31:0] addr_buf;
    logic [31:0] data_buf;

    // Rising Edge Detection
    logic rising_cs;

    // data from spi slave
    logic [31:0] recv_data;
    logic [7:0] recv_cmd;

    // counter
    logic [2:0] recv_counter;
    logic count_start;
    logic recv_running;

    // read address and data
    logic write_addr;
    logic write_data;
    logic [31:0] read_addr;
    logic [31:0] read_data;

    // --|cmd parsing|-----------------------------------------------------------
    assign recv_cmd = recv_data[7:0];

    // --|register update|-----------------------------------------------------------
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            read_addr <= '0;
            read_data <= '0;
        end else begin
            if (write_addr) begin
                read_addr <= recv_data;
            end else begin
                read_addr <= read_addr;
            end
            if (write_data) begin
                read_data <= recv_data;
            end else begin
                read_data <= read_data;
            end
        end
    end

    // --|counter|-----------------------------------------------------------
    assign recv_running = recv_counter != '0;
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            recv_counter <= '0;
        end else begin
            if (count_start) begin
                recv_counter <= 4;
            end else if (rising_cs && recv_running) begin    // while running
                recv_counter <= recv_counter - 1;
            end
        end
    end    

    // --|FSM|------------------------------------------------------------
    // state transition
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            curr_state <= IDLE;
        end else begin
            curr_state <= next_state;
        end
    end

    // next state logic 
    always_comb begin
        case (curr_state)
            IDLE: begin
                next_state = WAIT_CMD;
            end 
            WAIT_CMD: begin
                if (rising_cs) begin
                    case (recv_cmd)
                        8'h1: begin
                            next_state = READ_ADDR;
                        end
                        8'h2: begin
                            next_state = READ_DATA;
                        end 
                        default: begin
                            next_state = WAIT_CMD;
                        end
                    endcase
                end else begin  
                    next_state = WAIT_CMD;
                end
            end 
            READ_ADDR: begin
                if (recv_running) begin
                    next_state = READ_ADDR;
                end else begin
                    next_state = WAIT_CMD;
                end
            end
            READ_DATA: begin
                if (recv_running) begin
                    next_state = READ_DATA;
                end else begin
                    next_state = BUS_WRITE;
                end
            end 
            BUS_WRITE: begin
                next_state = WAIT_CMD;
            end
            default: begin
                next_state = IDLE;
            end
        endcase
    end


    // output logic 
    always_comb begin
        count_start = '0;
        req_spi_o = '0;
        write_addr = '0;
        write_data = '0;
        // bus interface
        spi_addr_o = '0;
        spi_wr_data_o = '0;
        spi_size_o = '0;
        spi_read_o = '0;
        spi_write_o = '0;
        case (curr_state)
            WAIT_CMD: begin
                if (rising_cs) begin
                    if ((recv_cmd == 8'h1) || (recv_cmd == 8'h2)) begin
                        count_start = 1'b1;
                    end else begin
                        count_start = '0;
                    end
                end else begin 
                    count_start = '0;
                end
            end
            READ_ADDR: begin
                if (recv_running) begin
                    write_addr = 1'b1;
                end else begin
                    write_addr = 1'b0;
                end
            end
            READ_DATA: begin
                if (recv_running) begin
                    write_data = 1'b1;
                end else begin
                    req_spi_o = 1'b1;
                    write_data = 1'b0;
                end
            end 
            BUS_WRITE: begin
                // if grant write data
                if (gnt_spi_i) begin
                    spi_addr_o = read_addr;
                    spi_wr_data_o = read_data;
                    spi_size_o = 4'b1111;
                    spi_write_o = 1'b1;
                end else begin
                    spi_addr_o = '0;
                    spi_wr_data_o = '0;
                    spi_size_o = '0;
                    spi_write_o = '0;
                end
            end
            default: begin
                count_start = '0;
                req_spi_o = '0;
                write_addr = '0;
                write_data = '0;
                // bus interface
                spi_addr_o = '0;
                spi_wr_data_o = '0;
                spi_size_o = '0;
                spi_read_o = '0;
                spi_write_o = '0;
            end
        endcase
    end


    rising_edge_detect red (
        .clk_i      (clk_i),
        .signal_i   (cs_i),
        .edge_o     (rising_cs)
    );
    
    spi_slave spi_slave(
        .clk_i      (clk_i),
        .rst_ni     (rst_ni),
        .sclk_i     (sclk_i),
        .ss_ni      (cs_i),
        .mosi_i     (mosi_i),
        .miso_o     (miso_o),
        // we only receive data from external spi master
        .data_i     (32'h0),
        .data_o     (recv_data)
    );

endmodule
