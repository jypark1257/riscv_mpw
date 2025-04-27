module spi_master (
    input  logic        clk,           // 250MHz input clock
    input  logic        rst_n,
    
    // Control signals
    input  logic        start,
    output logic        done,
    
    // Data signals
    input  logic [7:0]  data_in,
    output logic [7:0]  data_out,
    
    // SPI interface
    output logic        sclk,
    output logic        mosi,
    input  logic        miso,
    output logic        cs_n
);

    // Parameters
    localparam int CPOL = 0; // Clock polarity (0: idle low, 1: idle high)
    localparam int CPHA = 0; // Clock phase (0: sample on first edge, 1: sample on second edge)
    localparam int CLKS_PER_HALF_BIT = 25; // 250MHz / (2 * 1MHz) = 125
                                            // 250MHz / (2 * 5MHz) = 25

    // States
    typedef enum logic [1:0] {IDLE, TRANSFER, DONE} state_t;
    state_t state, next_state;

    // Registers
    logic [7:0] shift_reg;
    logic [3:0] bit_counter;
    logic [6:0] clk_counter;
    logic sclk_internal;

    logic data_change;
    assign data_change = CPHA ^ sclk_internal;

    // State machine
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    always_comb begin
        next_state = state;
        case (state)
            IDLE:     if (start) next_state = TRANSFER;
            TRANSFER: if (bit_counter == 4'b1000 && clk_counter == CLKS_PER_HALF_BIT-1) next_state = DONE;
            DONE:     next_state = IDLE;
			default: ;
		endcase
    end

    // SPI logic
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            shift_reg <= '0;
            bit_counter <= '0;
            clk_counter <= '0;
            sclk_internal <= CPOL;
            sclk <= CPOL;
            cs_n <= '1;
            done <= '0;
            data_out <= '0;
        end else begin
            unique case (state)
                IDLE: begin
                    sclk_internal <= CPOL;
                    sclk <= CPOL;
                    cs_n <= '1;
                    done <= '0;
                    if (start) begin
                        shift_reg <= data_in;
                        bit_counter <= '0;
                        clk_counter <= '0;
                        cs_n <= '0;
                    end
                end
                
                TRANSFER: begin
                    if (clk_counter == CLKS_PER_HALF_BIT-1) begin
                        clk_counter <= '0;
                        sclk_internal <= ~sclk_internal;
                        
                        if (CPHA ^ sclk_internal) begin
                            shift_reg <= {shift_reg[6:0], miso};
                            bit_counter <= bit_counter + 1'b1;
                        end
                    end else begin
                        clk_counter <= clk_counter + 1'b1;
                    end
                    
                    sclk <= sclk_internal;
                end
                
                DONE: begin
                    cs_n <= '1;
                    done <= '1;
                    data_out <= shift_reg;
                end
            endcase
        end
    end


    always @(*) begin
        case (state)
            TRANSFER: begin
                if (clk_counter == 7'h0C) begin
                    mosi = shift_reg[7];
                end
            end
        endcase
    end 

endmodule
