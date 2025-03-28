
module pim_dma #(
    parameter PIM_CTRL          = 32'h4000_0010,
    parameter PIM_R             = 32'h4000_0020,
    parameter PIM_W_WEIGHT      = 32'h4000_0040,
    parameter PIM_W_ACTIVATION  = 32'h4000_0080,
	parameter PIM_W_KEY			= 32'h4000_0100,
	parameter PIM_W_VREF		= 32'h4000_0200,
	parameter PIM_W_MODE		= 32'h4000_0400
) (
    input                   clk_i,
    input                   rst_ni,
    // DMA enable
    input                   dma_en_i,
    // pim instruction
    // 3'b001: pim_write
    // 3'b010: pim_compute
    // 3'b100: pim_load
    input           [2:0]   funct3_i,
    input           [3:0]   sel_pim_i,
    input           [12:0]  size_i,       // maximum available transfer count: 8192 (32K * byte)
    input           [31:0]  mem_addr_i,
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

    // FSM states
    typedef enum logic [2:0] { IDLE, RW_SETUP, R_EXE, RW_EXE, R_PIM_WAIT, R_PIM_EXE, RW_PIM_EXE } e_state;

    localparam FUNCT_WEIGHT = 2'b01;
    localparam FUNCT_ACT    = 2'b10;
    
    localparam PIM_WRITE    = 3'b001;    // write weight to pim
    localparam PIM_COMPUTE  = 3'b010;    // write activation to pim
    localparam PIM_LOAD     = 3'b100;   // load output result from pim
	localparam PIM_KEY		= 3'b101;
	localparam PIM_VREF		= 3'b110;
	localparam PIM_MODE		= 3'b111;
	
    // PIM status
    // logic pim_busy;
	logic pim_valid;
    logic pim_data_valid; 

    // request for operation?
    logic operation_start;

    // operand fetch
    logic [2:0] funct3;
    logic [3:0] sel_pim;
    logic [12:0] size;
    logic [31:0] mem_addr;

    // current state, next state
    e_state curr_state;
    e_state next_state;

    // counter
    logic [13:0] trans_counter;     // maximum available transfer count: 8192 (32K * byte)
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

    // --|PIM address select|-------------------------------------------------------------
    always_comb begin
		pim_write_addr = '0;
		pim_read_addr = '0;
        case (funct3)
            PIM_WRITE: pim_write_addr = PIM_W_WEIGHT | sel_pim;
            PIM_COMPUTE: pim_write_addr = PIM_W_ACTIVATION | sel_pim;
            PIM_LOAD: pim_read_addr = PIM_R | sel_pim;
			PIM_KEY: pim_write_addr = PIM_W_KEY | sel_pim;
			PIM_VREF: pim_write_addr = PIM_W_VREF | sel_pim;
			PIM_MODE: pim_write_addr = PIM_W_MODE | sel_pim;
			default: begin
                pim_write_addr = '0;
                pim_read_addr = '0;
            end
        endcase
    end

    // --|operand fetch|------------------------------------------------------------------
    assign operation_start = dma_en_i && (!trans_running);

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == '0) begin
            funct3 <= '0;
            sel_pim <= '0;
            size <= '0;
            mem_addr <= '0;
        end else begin
            if (operation_start) begin
                funct3 <= funct3_i;
                sel_pim <= sel_pim_i;
                size <= size_i;
                mem_addr <= mem_addr_i;
            end else begin
                funct3 <= funct3;
                sel_pim <= sel_pim;
                size <= size;
                // mem address increment
                if (mem_incr) begin
                    mem_addr <= mem_addr + 4;
                end else begin
                    mem_addr <= mem_addr;
                end
            end
        end
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
                    if ((funct3 == PIM_WRITE) || (funct3 == PIM_COMPUTE) || (funct3 == PIM_KEY) || (funct3 == PIM_VREF) || (funct3 == PIM_MODE)) begin
                        if (pim_valid) begin
                            next_state = R_EXE;
                        end else begin
                            next_state = RW_SETUP;
                        end
                    end else if (funct3 == PIM_LOAD) begin
                        if ((pim_valid) && pim_data_valid) begin
                            next_state = R_PIM_WAIT;
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
			R_PIM_WAIT: begin
				if (!bus_gnt_i) begin
					next_state = R_PIM_WAIT;
				end else begin
					next_state = R_PIM_EXE;
				end
			end
            R_PIM_EXE: begin
                if (!bus_gnt_i) begin
                    next_state = R_PIM_EXE;
                end else begin
                    next_state = RW_PIM_EXE;
                end
            end
            R_EXE: begin
                if (!bus_gnt_i) begin
                    next_state = R_EXE;
                end else begin      // bus_gnt && trans_running
                    next_state = RW_EXE;
                end
            end
            RW_EXE: begin
                if (!trans_running) begin   // go to W_EXE when transfer is done
                    next_state = IDLE;
                end else if (!bus_gnt_i) begin
                    next_state = RW_EXE;
                end else begin              // bus_gnt
                    next_state = RW_EXE;
                end
            end
            RW_PIM_EXE: begin
                if (!trans_running) begin   // go to W_EXE when transfer is done
                    next_state = IDLE;
                end else if (!bus_gnt_i) begin
                    next_state = RW_PIM_EXE;
                end else begin              // bus_gnt
                    next_state = RW_PIM_EXE;
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
                count_start = 1'b1;
                // read PIM control signal
                dma_addr_1_o = PIM_CTRL;
                dma_write_1_o = '0;
                dma_read_1_o = 1'b1;
                dma_size_1_o = 4'b1111;
                dma_wr_data_1_o = '0;
            end
			R_PIM_WAIT: begin
				dma_busy_o = 1'b1;
				bus_req_o = 1'b1;
				if (bus_gnt_i) begin
					cnt_decr = 1'b0;
					mem_incr = 1'b0;
					// DMA SRAM I/F
					dma_addr_0_o = '0;
					dma_write_0_o = '0;
					dma_read_0_o = '0;
					dma_size_0_o = 4'b1111;
					dma_wr_data_0_o = '0;

					dma_addr_1_o = pim_read_addr;
					dma_write_1_o = 1'b0;
					dma_read_1_o = 1'b1;
					dma_size_1_o = 4'b1111;
					dma_wr_data_1_o = '0;
				end else begin
					cnt_decr = 1'b0;
					mem_incr = 1'b0;
					dma_addr_0_o = '0;
					dma_write_0_o = '0;
					dma_read_0_o = '0;
					dma_size_0_o =  4'b1111;
					dma_wr_data_0_o = '0;

					dma_addr_1_o = '0;
					dma_write_1_o = '0;
					dma_read_1_o = '0;
					dma_size_1_o = 4'b1111;
					dma_wr_data_1_o = '0;
				end
			end
            R_PIM_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin
                    cnt_decr = 1'b1;
                    mem_incr = 1'b0;
                    // DMA SRAM I/F
                    dma_addr_0_o = '0;
                    dma_write_0_o = '0;
                    dma_read_0_o = '0;
                    dma_size_0_o = 4'b1111;
                    dma_wr_data_0_o = '0;

                    dma_addr_1_o = pim_read_addr;
                    dma_write_1_o = 1'b0;
                    dma_read_1_o = 1'b1;
                    dma_size_1_o = 4'b1111;
                    dma_wr_data_1_o = '0;
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
            R_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin
                    cnt_decr = 1'b1;
                    mem_incr = 1'b1;
                    // DMA SRAM I/F
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
                    // DMA SRAM I/F
                    dma_addr_0_o = (!trans_running) ? '0 : mem_addr;
                    dma_write_0_o = 1'b0;
                    dma_read_0_o = (!trans_running) ? 1'b0 : 1'b1;
                    dma_size_0_o = 4'b1111;
                    dma_wr_data_0_o = '0;
            
                    dma_addr_1_o = pim_write_addr;
                    dma_write_1_o = 1'b1;
                    dma_read_1_o = 1'b0;
                    dma_size_1_o = 4'b1111;
                    dma_wr_data_1_o = dma_rd_data_0_i;
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
            RW_PIM_EXE: begin
                dma_busy_o = 1'b1;
                bus_req_o = 1'b1;
                if (bus_gnt_i) begin   
                    cnt_decr = 1'b1;    
                    mem_incr = 1'b1;             
                    // DMA SRAM I/F
                    dma_addr_0_o = mem_addr;
                    dma_write_0_o = 1'b1;
                    dma_read_0_o = '0;
                    dma_size_0_o = 4'b1111;
                    dma_wr_data_0_o = dma_rd_data_1_i;
        
                    dma_addr_1_o = (!trans_running) ? '0 : pim_read_addr;
                    dma_write_1_o = 1'b0;
                    dma_read_1_o = (!trans_running) ? '0 : 1'b1;
                    dma_size_1_o = 4'b1111;
                    dma_wr_data_1_o = '0;
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
