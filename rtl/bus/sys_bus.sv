module sys_bus (
    input                   clk_i, 
    input                   rst_ni,

    // RV IMEM
    input           [31:0]  imem_addr_i,
    input                   imem_write_i,
    input                   imem_read_i,
    input           [ 3:0]  imem_size_i,
    input           [31:0]  imem_din_i,
    output logic    [31:0]  imem_dout_o,

    // SPI SLAVE
    input                   req_spi_i,
    output                  gnt_spi_o,
    input           [31:0]  spi_addr_i,
    input                   spi_write_i,
    input                   spi_read_i,
    input           [ 3:0]  spi_size_i,
    input           [31:0]  spi_din_i,
    output logic    [31:0]  spi_dout_o,

    // RV DMEM
    input                   req_dmem_i,
    output                  gnt_dmem_o,
    input           [31:0]  dmem_addr_i,
    input                   dmem_write_i,
    input                   dmem_read_i,
    input           [ 3:0]  dmem_size_i,
    input           [31:0]  dmem_din_i,
    output logic    [31:0]  dmem_dout_o,

    // DMA
    input                   req_dma_i,
    output                  gnt_dma_o,
    input           [31:0]  dma_addr_0_i,
    input                   dma_write_0_i,
    input                   dma_read_0_i,
    input           [ 3:0]  dma_size_0_i,
    input           [31:0]  dma_din_0_i,
    output logic    [31:0]  dma_dout_0_o,
    input           [31:0]  dma_addr_1_i,
    input                   dma_write_1_i,
    input                   dma_read_1_i,
    input           [ 3:0]  dma_size_1_i,
    input           [31:0]  dma_din_1_i,
    output logic    [31:0]  dma_dout_1_o,

    // IMEM SRAM (IMEM port)
    output logic    [31:0]  imem_addr_o,
    output logic            imem_write_o,
    output logic            imem_read_o,
    output logic    [ 3:0]  imem_size_o,
    output logic    [31:0]  imem_din_o,
    input           [31:0]  imem_dout_i,

    // DMEM SRAM (DMEM port)
    output logic    [31:0]  dmem_addr_o,
    output logic            dmem_write_o,
    output logic            dmem_read_o,
    output logic    [ 3:0]  dmem_size_o,
    output logic    [31:0]  dmem_din_o,
    input           [31:0]  dmem_dout_i,

    // PIM BUFFER SRAM
    output logic    [31:0]  buf_addr_0_o,
    output logic            buf_write_0_o,
    output logic            buf_read_0_o,
    output logic    [ 3:0]  buf_size_0_o,
    output logic    [31:0]  buf_din_0_o,
    input           [31:0]  buf_dout_0_i,

    output logic    [31:0]  buf_addr_1_o,
    output logic            buf_write_1_o,
    output logic            buf_read_1_o,
    output logic    [ 3:0]  buf_size_1_o,
    output logic    [31:0]  buf_din_1_o,
    input           [31:0]  buf_dout_1_i,

    // UART
    output logic    [31:0]  uart_addr_o,
    output logic            uart_write_o,
    output logic            uart_read_o,
    output logic    [ 3:0]  uart_size_o,
    output logic    [31:0]  uart_din_o,
    input           [31:0]  uart_dout_i,

    // Hybrid-PIM_0
    output logic    [31:0]  pim_addr_o,
    output logic            pim_write_o,
    output logic            pim_read_o,
    output logic    [ 3:0]  pim_size_o,
    output logic    [31:0]  pim_din_o,
    input           [31:0]  pim_dout_i
);

    // ---------------- Address Map (new) ----------------
    // IMEM : [0x1000_0000, 0x1000_4000)
    // DMEM : [0x1000_4000, 0x1000_8000)
    localparam logic [31:0] IMEM_BASE = 32'h1000_0000;
    localparam logic [31:0] IMEM_END  = 32'h1000_4000; // exclusive
    localparam logic [31:0] DMEM_BASE = 32'h1000_4000;
    localparam logic [31:0] DMEM_END  = 32'h1000_8000; // exclusive

    // latch dmem/dma addresses
    logic [31:0] dmem_addr_q;
    logic [31:0] dma_addr_0_q;
    logic [31:0] dma_addr_1_q;

    // internal grant signal 
    logic gnt_imem;

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (~rst_ni) begin
            dmem_addr_q  <= '0;
            dma_addr_0_q <= '0;
            dma_addr_1_q <= '0;
        end else begin
            dmem_addr_q  <= dmem_addr_i;
            dma_addr_0_q <= dma_addr_0_i;
            dma_addr_1_q <= dma_addr_1_i;
        end
    end

    // priority arbiter
    bus_arbiter arbiter (
        .clk_i      (clk_i),
        .rst_ni     (rst_ni),

        .req_spi_i  (req_spi_i),
        .gnt_spi_o  (gnt_spi_o),

        .req_dmem_i (req_dmem_i),
        .gnt_dmem_o (gnt_dmem_o),

        .req_dma_i  (req_dma_i),
        .gnt_dma_o  (gnt_dma_o)
    );

    // SPI가 IMEM 윈도우를 접근 중이면 RV-IMEM에 그랜트 주지 않음 (function 제거, 직접 조건식 사용)
    assign gnt_imem = !( gnt_spi_o && (spi_addr_i >= IMEM_BASE) && (spi_addr_i < IMEM_END) );

    // IMEM master mux (RV or SPI)
    assign imem_addr_o  = (gnt_imem) ? imem_addr_i : spi_addr_i;
    assign imem_read_o  = (gnt_imem) ? imem_read_i : spi_read_i;
    assign imem_write_o = (gnt_imem) ? imem_write_i : spi_write_i;
    assign imem_size_o  = (gnt_imem) ? imem_size_i : spi_size_i;
    assign imem_din_o   = (gnt_imem) ? imem_din_i  : spi_din_i;

    // ---------------- SLAVE DMEM PORT (write/read cmds out) ----------------
    always @(*) begin
        dmem_addr_o  = '0;
        dmem_write_o = '0;
        dmem_read_o  = '0;
        dmem_size_o  = '0;
        dmem_din_o   = '0;

        uart_addr_o  = '0;
        uart_write_o = '0;
        uart_read_o  = '0;
        uart_size_o  = '0;
        uart_din_o   = '0;

        buf_addr_0_o = '0;
        buf_write_0_o= '0;
        buf_read_0_o = '0;
        buf_size_0_o = '0;
        buf_din_0_o  = '0;

        buf_addr_1_o = '0;
        buf_write_1_o= '0;
        buf_read_1_o = '0;
        buf_size_1_o = '0;
        buf_din_1_o  = '0;

        pim_addr_o   = '0;
        pim_write_o  = '0;
        pim_read_o   = '0;
        pim_size_o   = '0;
        pim_din_o    = '0;

        case ({gnt_spi_o, gnt_dmem_o, gnt_dma_o})
            3'b100: begin   // SPI GRANTED
                case (spi_addr_i[31:28])
                    4'h1: begin // SPI → DMEM window만 허용
                        if ( (spi_addr_i >= DMEM_BASE) && (spi_addr_i < DMEM_END) ) begin
                            dmem_addr_o  = spi_addr_i;
                            dmem_write_o = spi_write_i;
                            dmem_read_o  = spi_read_i;
                            dmem_size_o  = spi_size_i;
                            dmem_din_o   = spi_din_i;
                        end
                    end
                    4'h2: begin // SPI → PIM_BUFFER
                        case (spi_addr_i[14]) 
                            1'b0: begin
                                buf_addr_0_o  = spi_addr_i;
                                buf_write_0_o = spi_write_i;
                                buf_read_0_o  = spi_read_i;
                                buf_size_0_o  = spi_size_i;
                                buf_din_0_o   = spi_din_i;
                            end
                            1'b1: begin
                                buf_addr_1_o  = spi_addr_i;
                                buf_write_1_o = spi_write_i;
                                buf_read_1_o  = spi_read_i;
                                buf_size_1_o  = spi_size_i;
                                buf_din_1_o   = spi_din_i;
                            end
                        endcase
                    end
                    4'h4: begin // SPI → PIM
                        pim_addr_o  = spi_addr_i;
                        pim_write_o = spi_write_i;
                        pim_read_o  = spi_read_i;
                        pim_size_o  = spi_size_i;
                        pim_din_o   = spi_din_i;
                    end
                    default: begin
                        // 기존 동작 유지: 기타는 DMEM 포트로 패스스루
                        dmem_addr_o  = spi_addr_i;
                        dmem_write_o = spi_write_i;
                        dmem_read_o  = spi_read_i;
                        dmem_size_o  = spi_size_i;
                        dmem_din_o   = spi_din_i;
                    end
                endcase
            end

            3'b010: begin    // RV DMEM GRANTED
                case (dmem_addr_i[31:28])
                    4'h1: begin // RV → DMEM window만 허용
                        if ( (dmem_addr_i >= DMEM_BASE) && (dmem_addr_i < DMEM_END) ) begin
                            dmem_addr_o  = dmem_addr_i;
                            dmem_write_o = dmem_write_i;
                            dmem_read_o  = dmem_read_i;
                            dmem_size_o  = dmem_size_i;
                            dmem_din_o   = dmem_din_i;
                        end
                    end
                    4'h2: begin // RV → PIM_BUFFER
                        case (dmem_addr_i[14])
                            1'b0: begin
                                buf_addr_0_o  = dmem_addr_i;
                                buf_write_0_o = dmem_write_i;
                                buf_read_0_o  = dmem_read_i;
                                buf_size_0_o  = dmem_size_i;
                                buf_din_0_o   = dmem_din_i;
                            end
                            1'b1: begin
                                buf_addr_1_o  = dmem_addr_i;
                                buf_write_1_o = dmem_write_i;
                                buf_read_1_o  = dmem_read_i;
                                buf_size_1_o  = dmem_size_i;
                                buf_din_1_o   = dmem_din_i;
                            end
                        endcase
                    end
                    4'h8: begin // RV → UART
                        uart_addr_o  = dmem_addr_i;
                        uart_write_o = dmem_write_i;
                        uart_read_o  = dmem_read_i;
                        uart_size_o  = dmem_size_i;
                        uart_din_o   = dmem_din_i;
                    end
                    default: begin
                        // 기타는 기존처럼 DMEM 포트로 전달
                        dmem_addr_o  = dmem_addr_i;
                        dmem_write_o = dmem_write_i;
                        dmem_read_o  = dmem_read_i;
                        dmem_size_o  = dmem_size_i;
                        dmem_din_o   = dmem_din_i;
                    end
                endcase
            end

            3'b001: begin    // DMA GRANTED
                // DMA0 → PIM_BUFFER
                case (dma_addr_0_i[31:28])
                    4'h2: begin
                        case (dma_addr_0_i[14])
                            1'b0: begin
                                buf_addr_0_o  = dma_addr_0_i;
                                buf_write_0_o = dma_write_0_i;
                                buf_read_0_o  = dma_read_0_i;
                                buf_size_0_o  = dma_size_0_i;
                                buf_din_0_o   = dma_din_0_i;
                            end 
                            1'b1: begin
                                buf_addr_1_o  = dma_addr_0_i;
                                buf_write_1_o = dma_write_0_i;
                                buf_read_1_o  = dma_read_0_i;
                                buf_size_1_o  = dma_size_0_i;
                                buf_din_1_o   = dma_din_0_i;
                            end
                        endcase
                    end
                    default: begin
                        // no-op
                    end
                endcase
                // DMA1 → PIM
                case (dma_addr_1_i[31:28])
                    4'h4: begin
                        pim_addr_o  = dma_addr_1_i;
                        pim_write_o = dma_write_1_i;
                        pim_read_o  = dma_read_1_i;
                        pim_size_o  = dma_size_1_i;
                        pim_din_o   = dma_din_1_i;
                    end
                    default: begin
                        // no-op
                    end
                endcase
            end

            default: begin
                // 기본: RV DMEM 신호 패스스루
                dmem_addr_o  = dmem_addr_i;
                dmem_write_o = dmem_write_i;
                dmem_read_o  = dmem_read_i;
                dmem_size_o  = dmem_size_i;
                dmem_din_o   = dmem_din_i;
            end
        endcase
    end
    
    // ---------------- SLAVES' DOUT ----------------
    // SPI SLAVE, assign zero output
    assign spi_dout_o = '0;

    // MASTER RV IMEM PORT
    assign imem_dout_o = imem_dout_i;

    // MASTER RV DMEM PORT (read data mux) — function 없이 직접 범위 비교
    always @(*) begin
        dmem_dout_o = '0;
        unique case (1'b1)
            ((dmem_addr_q >= DMEM_BASE) && (dmem_addr_q < DMEM_END)): begin
                dmem_dout_o = dmem_dout_i;       // DMEM 창
            end
            (dmem_addr_q[31:28] == 4'h2): begin  // PIM_BUFFER
                case (dmem_addr_q[14]) 
                    1'b0: dmem_dout_o = buf_dout_0_i;
                    1'b1: dmem_dout_o = buf_dout_1_i;
                endcase
            end
            (dmem_addr_q[31:28] == 4'h8): begin  // UART
                dmem_dout_o = uart_dout_i;
            end
            default: begin
                dmem_dout_o = dmem_dout_i;       // 기타는 기존 동작 유지
            end
        endcase
    end
    
    // MASTER RV DMA PORT (read data mux)
    always @(*) begin
        dma_dout_0_o = '0;
        dma_dout_1_o = '0;

        case (dma_addr_0_q[31:28])
            4'h2: begin
                case (dma_addr_0_q[14]) 
                    1'b0: dma_dout_0_o = buf_dout_0_i;
                    1'b1: dma_dout_0_o = buf_dout_1_i;
                endcase
            end 
            default: begin
                dma_dout_0_o = '0;
            end
        endcase

        case (dma_addr_1_q[31:28])
            4'h4: dma_dout_1_o = pim_dout_i;
            default: dma_dout_1_o = '0;
        endcase
    end

endmodule
