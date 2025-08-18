
module pim_dma_v2 #(
    parameter PIM_BASE_ADDR = 32'h4000_0000,    // PIM base address
    parameter PIM_MODE      = 32'h4100_0000,    // PIM mode write address
    parameter PIM_ZP_ADDR   = 32'h4200_0000,    // PIM zero-point address
    parameter PIM_STATUS    = 32'h4300_0000     // PIM status read address
) (
    input                   clk_i,
    input                   rst_ni,
    // DMA enable
    input                   dma_en_i,
    // funct3
    // 3'b001: PIM_ERASE
    // 3'b010: PIM_PROGRAM
    // 3'b011: PIM_READ
    // 3'b100: PIM_ZP
    // 3'b101: PIM_PARALLEL
    // 3'b110: PIM_RBR
    // 3'b111: PIM_LOAD
    input           [2:0]   funct3_i,
    // immediate12 (sel_pim)
    input           [11:0]  imm_i,
    // rs1 (row/col address)
    input           [31:0]  rs1_i,
    // rs2 (timing/count or buffer_addr.)
    input           [31:0]  rs2_i,
    // bus request 
    output  logic           bus_req_o,
    input                   bus_gnt_i,
    // bus interface (SRAM)
    output  logic   [31:0]  dma_addr_0_o,
    output  logic           dma_write_0_o,
    output  logic           dma_read_0_o,
    output  logic   [3:0]   dma_size_0_o,
    output  logic   [31:0]  dma_wr_data_0_o,
    input           [31:0]  dma_rd_data_0_i,
    // bus interface (PIM)
    output  logic   [31:0]  dma_addr_1_o,
    output  logic           dma_write_1_o,
    output  logic           dma_read_1_o,
    output  logic   [3:0]   dma_size_1_o,
    output  logic   [31:0]  dma_wr_data_1_o,
    input           [31:0]  dma_rd_data_1_i,
    // DMA status
    output  logic           dma_busy_o
);

    // PIM operation codes
    localparam PIM_ERASE    = 3'b001;   // PIM_ERASE
    localparam PIM_PROGRAM  = 3'b010;   // PIM_PROGRAM
    localparam PIM_READ     = 3'b011;   // PIM_READ
	localparam PIM_ZP       = 3'b100;   // PIM_ZP
	localparam PIM_PARALLEL = 3'b101;   // PIM_PARALLEL
	localparam PIM_RBR      = 3'b110;   // PIM_RBR
	localparam PIM_LOAD     = 3'b111;   // PIM_LOAD

    // PIM transfer size (W)
    localparam int SIZE_ERASE       = 1;
    localparam int SIZE_PROGRAM     = 1;
    localparam int SIZE_ZP          = 1;
    localparam int SIZE_PARALLEL    = 16;
    localparam int SIZE_RBR         = 2;

    // PIM transfer size (R)
    localparam int SIZE_READ            = 1; 
    localparam int SIZE_LOAD_PARALLEL   = 64;
    localparam int SIZE_LOAD_RBR        = 32;

    // FSM states
    // 3'b000: IDLE
    // 3'b001: RW_SETUP
    // 3'b010: MODE_EXE
    // 3'b011: R_EXE
    // 3'b100: RW_EXE
    // 3'b101: W_EXE
    typedef enum logic [2:0] { IDLE, RW_SETUP, MODE_EXE, R_EXE, RW_EXE, W_EXE } e_state;

    // PIM status
    // logic pim_busy;
	logic pim_valid;
    logic pim_data_valid; 

    // request for operation?
    logic operation_start;

    // operand fetch
    logic [31:0] rc_addr; // row/col address
    logic [2:0] funct3;
    logic [11:0] sel_pim;
    logic [12:0] size;
    logic [31:0] mem_addr;
    logic [31:0] timing_count;
    logic [31:0] zero_point;

    // current state, next state
    e_state curr_state;
    e_state next_state;

    // counter
    logic [13:0] trans_counter;     // maximum available transfer count: 8192 (32K * byte)
    logic [13:0] rev_trans_counter;     // maximum available transfer count: 8192 (32K * byte)
    logic count_start;
    logic [13:0] data_count;   // GENERATE FROM FSM
    logic trans_running;

    // control signals
    logic mem_incr;
    logic cnt_decr;
    
    // PIM address
    logic [31:0] pim_write_addr;
    logic [31:0] pim_read_addr;
    
    // --|PIM status|--------------------------------------------------------------------
    // transfer data when       (pim_valid)
    // load data from pim when  (pim_valid) && (pim_data_valid) 
    // assign pim_busy = dma_rd_data_1_i[0];
	assign pim_valid = dma_rd_data_1_i[0];
	assign pim_data_valid = dma_rd_data_1_i[1];


    // --|operand fetch|------------------------------------------------------------------
    assign operation_start = dma_en_i && (!trans_running);

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            size <= '0;
        end else begin
            if (operation_start) begin
                case (funct3_i)
                    PIM_ERASE: size <= SIZE_ERASE;
                    PIM_PROGRAM: size <= SIZE_PROGRAM;
                    PIM_ZP: size <= SIZE_ZP;
                    PIM_READ: size <= SIZE_READ;
                    PIM_PARALLEL: size <= SIZE_PARALLEL;
                    PIM_RBR: size <= SIZE_RBR;
                    PIM_LOAD: begin
                        if (rs1_i == 32'h1) begin
                            size <= SIZE_LOAD_PARALLEL; // load parallel data
                        end else if (rs1_i == 32'h2) begin
                            size <= SIZE_LOAD_RBR; // load RBR data
                        end else begin
                            size <= '0;
                        end
                    end
                    default: size <= '0;
                endcase
            end else begin
                size <= size;
            end
        end
    end
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            rc_addr <= '0;
            funct3 <= '0;
            sel_pim <= '0;
            mem_addr <= '0;
            timing_count <= '0;
            zero_point <= '0;
        end else begin
            if (operation_start) begin
                rc_addr <= rs1_i; // row/col address
                funct3 <= funct3_i;
                sel_pim <= imm_i;
                mem_addr <= rs2_i;
                timing_count <= rs2_i;
                zero_point <= rs2_i;
            end else begin
                rc_addr <= rc_addr;
                funct3 <= funct3;
                sel_pim <= sel_pim;
                // mem address increment
                if (mem_incr) begin
                    mem_addr <= mem_addr + 4;
                end else begin
                    mem_addr <= mem_addr;
                end
                timing_count <= timing_count;
                zero_point <= zero_point;
            end
        end
    end

    // --|PIM address select|-------------------------------------------------------------
    always @(*) begin
		pim_write_addr = '0;
		pim_read_addr = '0;
        case (funct3)
            PIM_ERASE: pim_write_addr = PIM_BASE_ADDR + rc_addr;
            PIM_PROGRAM: pim_write_addr = PIM_BASE_ADDR + rc_addr;
            PIM_ZP: pim_write_addr = PIM_ZP_ADDR;
            PIM_READ: pim_read_addr = PIM_BASE_ADDR + rc_addr;
            PIM_PARALLEL: pim_write_addr = (PIM_BASE_ADDR + rc_addr) | ({16'h0, rev_trans_counter[3:0], 12'h0});
            PIM_RBR: pim_write_addr = (PIM_BASE_ADDR + rc_addr) | ({16'h0, rev_trans_counter[3:0], 12'h0});
            PIM_LOAD: pim_read_addr = PIM_BASE_ADDR + rc_addr;
			default: begin
                pim_write_addr = '0;
                pim_read_addr = '0;
            end
        endcase
    end

    // --|counter|-----------------------------------------------------------
    assign trans_running = trans_counter != '0;
    assign data_count = size;
    
    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            trans_counter <= '0;
        end else begin
            if (count_start) begin
                trans_counter <= data_count;
            end else if (cnt_decr && trans_running) begin    // while running
                trans_counter <= trans_counter - 1;
            end
        end
    end    

    always_comb begin
        rev_trans_counter = '0;
        case (funct3)
            PIM_PARALLEL: rev_trans_counter = 15 - trans_counter;
            PIM_RBR: rev_trans_counter = 1 - trans_counter;
            default: rev_trans_counter = '0;
        endcase
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
                if (operation_start) begin
                    next_state = RW_SETUP;
                end else begin
                    next_state = IDLE;
                end
            end
            RW_SETUP: begin
                if (bus_gnt_i) begin
                    if ((funct3 == PIM_ERASE) || (funct3 == PIM_PROGRAM) || (funct3 == PIM_ZP) || (funct3 == PIM_PARALLEL) || (funct3 == PIM_RBR)) begin
                        if (pim_valid) begin
                            next_state = MODE_EXE;
                        end else begin
                            next_state = RW_SETUP;
                        end
                    end else if ((funct3 == PIM_LOAD) ||(funct3 == PIM_READ)) begin
                        if (pim_valid && pim_data_valid) begin
                            next_state = MODE_EXE;
                        end else begin
                            next_state = RW_SETUP;
                        end
                    end else begin
                        next_state = RW_SETUP;
                    end
                end else begin
                    next_state = RW_SETUP;
                end
            end
            MODE_EXE: begin
                if (!bus_gnt_i) begin
                    next_state = MODE_EXE;
                end else if ((funct3 == PIM_ERASE) || (funct3 == PIM_PROGRAM) || (funct3 == PIM_ZP)) begin
                    next_state = W_EXE;
                end else begin      // bus_gnt && trans_running
                    next_state = R_EXE;
                end
            end
            R_EXE: begin
                if (!bus_gnt_i) begin
                    next_state = R_EXE;
                end else if (funct3 == PIM_READ) begin
                    next_state = W_EXE;
                end else begin      // bus_gnt && trans_running
                    next_state = RW_EXE;
                end
            end
            RW_EXE: begin
                if (!trans_running) begin   
                    next_state = IDLE;
                end else if (!bus_gnt_i) begin
                    next_state = RW_EXE;
                end else begin              // bus_gnt
                    next_state = RW_EXE;
                end
            end
            W_EXE: begin
                if (!trans_running) begin   
                    next_state = IDLE;
                end else if (!bus_gnt_i) begin
                    next_state = W_EXE;
                end else begin              // bus_gnt
                    next_state = W_EXE;
                end
            end
            default: begin
                next_state = IDLE;
            end
        endcase
    end 
    
    // output logic
    always_comb begin
        dma_busy_o = '0;
        bus_req_o = '0;
        count_start = '0;
        cnt_decr = '0;
        mem_incr = '0;
        // DMA SRAM I/F
        dma_addr_0_o = '0;
        dma_write_0_o = '0;
        dma_read_0_o = '0;
        dma_size_0_o = '0;
        dma_wr_data_0_o = '0;
        // DMA PIM I/F
        dma_addr_1_o = '0;
        dma_write_1_o = '0;
        dma_read_1_o = '0;
        dma_size_1_o = '0;
        dma_wr_data_1_o = '0;
        case (curr_state)
            RW_SETUP: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                count_start = 1'b0;
                // read PIM control signal
                dma_addr_1_o = PIM_STATUS;
                dma_write_1_o = '0;
                dma_read_1_o = 1'b1;
                dma_size_1_o = 4'b1111;
                dma_wr_data_1_o = '0;
            end
            MODE_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                count_start = 1'b1;
                // write PIM mode
                dma_addr_1_o = PIM_MODE;
                dma_write_1_o = 1'b1;
                dma_read_1_o = 1'b0;
                dma_size_1_o = 4'b1111;
                dma_wr_data_1_o = {29'b0, funct3};
            end
            R_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin
                    cnt_decr = 1'b1;
                    mem_incr = 1'b1;
                    if ((funct3 == PIM_LOAD) ||(funct3 == PIM_READ)) begin
                        dma_addr_0_o = '0;
                        dma_write_0_o = 1'b0;
                        dma_read_0_o = 1'b0;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = '0;

                        dma_addr_1_o =  pim_read_addr;
                        dma_write_1_o = '0;
                        dma_read_1_o = 1'b1;
                        dma_size_1_o = 4'b1111;
                        dma_wr_data_1_o = '0;
                    end else begin
                        dma_addr_0_o = mem_addr;
                        dma_write_0_o = 1'b0;
                        dma_read_0_o = 1'b1;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = '0;

                        dma_addr_1_o = '0;
                        dma_write_1_o = '0;
                        dma_read_1_o = '0;
                        dma_size_1_o = 4'b1111;
                        dma_wr_data_1_o = '0;
                    end
                end else begin
                    cnt_decr = '0;    
                    mem_incr = '0;         
                    dma_addr_0_o = '0;
                    dma_write_0_o = '0;
                    dma_read_0_o = '0;
                    dma_size_0_o = '0;
                    dma_wr_data_0_o = '0;

                    dma_addr_1_o = '0;
                    dma_write_1_o = '0;
                    dma_read_1_o = '0;
                    dma_size_1_o = '0;
                    dma_wr_data_1_o = '0;
                end
            end
            RW_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin   
                    cnt_decr = 1'b1;    
                    mem_incr = 1'b1;
                    if (funct3 == PIM_LOAD) begin
                        dma_addr_0_o = mem_addr;
                        dma_write_0_o = 1'b1;
                        dma_read_0_o = 1'b0;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = dma_rd_data_1_i;

                        dma_addr_1_o = pim_read_addr;
                        dma_write_1_o = 1'b0;
                        dma_read_1_o = 1'b1;
                        dma_size_1_o = 4'b1111;
                        dma_wr_data_1_o = '0;
                    end else begin
                        dma_addr_0_o = mem_addr;
                        dma_write_0_o = 1'b0;
                        dma_read_0_o = 1'b1;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = '0;

                        dma_addr_1_o = pim_write_addr;
                        dma_write_1_o = 1'b1;
                        dma_read_1_o = 1'b0;
                        dma_size_1_o = 4'b1111;
                        dma_wr_data_1_o = dma_rd_data_0_i;
                    end 
                end else begin
                    cnt_decr = '0;    
                    mem_incr = '0;         
                    dma_addr_0_o = '0;
                    dma_write_0_o = '0;
                    dma_read_0_o = '0;
                    dma_size_0_o = '0;
                    dma_wr_data_0_o = '0;
                    dma_addr_1_o = '0;
                    dma_write_1_o = '0;
                    dma_read_1_o = '0;
                    dma_size_1_o = '0;
                    dma_wr_data_1_o = '0;
                end
            end
            W_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin   
                    cnt_decr = 1'b1;    
                    mem_incr = 1'b1;
                    if ((funct3 == PIM_LOAD) || (funct3 == PIM_READ)) begin
                        dma_addr_0_o = mem_addr;
                        dma_write_0_o = 1'b1;
                        dma_read_0_o = 1'b0;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = dma_rd_data_1_i;

                        dma_addr_1_o = '0;
                        dma_write_1_o = 1'b0;
                        dma_read_1_o = 1'b0;
                        dma_size_1_o = 4'b1111;
                        dma_wr_data_1_o = '0;
                    end else begin
                        dma_addr_0_o = '0;
                        dma_write_0_o = 1'b0;
                        dma_read_0_o = 1'b0;
                        dma_size_0_o = 4'b1111;
                        dma_wr_data_0_o = '0;

                        dma_addr_1_o = pim_write_addr;
                        dma_write_1_o = 1'b1;
                        dma_read_1_o = 1'b0;
                        dma_size_1_o = 4'b1111;
                        if ((funct3 == PIM_ERASE) || (funct3 == PIM_PROGRAM)) begin
                            dma_wr_data_1_o = timing_count;
                        end else if (funct3 == PIM_ZP) begin
                            dma_wr_data_1_o = zero_point;
                        end else begin
                            dma_wr_data_1_o = dma_rd_data_0_i;
                        end
                    end 
                end else begin
                    cnt_decr = '0;    
                    mem_incr = '0;         
                    dma_addr_0_o = '0;
                    dma_write_0_o = '0;
                    dma_read_0_o = '0;
                    dma_size_0_o = '0;
                    dma_wr_data_0_o = '0;
                    dma_addr_1_o = '0;
                    dma_write_1_o = '0;
                    dma_read_1_o = '0;
                    dma_size_1_o = '0;
                    dma_wr_data_1_o = '0;
                end
            end
            default: begin
                dma_busy_o = '0;
                bus_req_o = '0;
                count_start = '0;
                mem_incr = '0;
                cnt_decr = '0;
                dma_addr_0_o = '0;
                dma_write_0_o = '0;
                dma_read_0_o = '0;
                dma_size_0_o = '0;
                dma_wr_data_0_o = '0;
                dma_addr_1_o = '0;
                dma_write_1_o = '0;
                dma_read_1_o = '0;
                dma_size_1_o = '0;
                dma_wr_data_1_o = '0;
            end
        endcase
    end
endmodule
