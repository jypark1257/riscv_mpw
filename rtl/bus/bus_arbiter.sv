
module bus_arbiter (
    input           clk_i,
    input           rst_ni,

    // master 1 (SPI)
    input           req_spi_i,
    output logic    gnt_spi_o,

    // master 2 (DMEM)
    input           req_dmem_i,
    output logic    gnt_dmem_o,

    // master 3 (DMA)
    input           req_dma_i,
    output logic    gnt_dma_o
);

    localparam IDLE     = 2'b00;
    localparam GNT_SPI  = 2'b01;
    localparam GNT_RV   = 2'b10;   // RV grant
    localparam GNT_DMA  = 2'b11;   // DMA grant

    logic [1:0] curr_state;
    logic [1:0] next_state;

    // state machine
    always_ff @ (posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            curr_state <= IDLE;
        end else begin
            curr_state <= next_state;
        end
    end

    // next state machine
    always_comb begin
        case (curr_state)
            IDLE: begin
                if (req_spi_i) begin
                    next_state = GNT_SPI;
                end else if (req_dma_i) begin
                    next_state = GNT_DMA;
                end else if (req_dmem_i) begin
                    next_state = GNT_RV;
                end else begin
                    next_state = IDLE;
                end
            end
            GNT_SPI: begin
                if (req_spi_i) begin
                    next_state = GNT_SPI;
                end else begin
                    next_state = IDLE;
                end
            end
            GNT_DMA: begin
                if (req_dma_i) begin
                    next_state = GNT_DMA;
                end else begin
                    next_state = IDLE;
                end
            end 
            GNT_RV: begin
                if (req_dmem_i) begin
                    next_state = GNT_RV;
                end else begin
                    next_state = IDLE;
                end
            end
	        // DEFAULT branch of CASE statement cannot be reached
            //default: begin
            //    next_state = IDLE;
            //end
        endcase
    end

    // state output machine
    always_comb begin
        gnt_spi_o = '0;
        gnt_dmem_o = '0;
        gnt_dma_o = '0;
        case (curr_state)
            GNT_SPI: begin
                gnt_spi_o = 1'b1;
            end
            GNT_RV: begin                    // RV grant (DMEM)
                gnt_dmem_o = 1'b1;
            end
            GNT_DMA: begin                    // DMA grant
                gnt_dma_o = 1'b1;
            end 
            default: begin
                gnt_spi_o = '0;
                gnt_dmem_o = '0;
                gnt_dma_o = '0;
            end
        endcase
    end
    


endmodule
