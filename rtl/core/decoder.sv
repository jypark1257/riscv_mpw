`include "opcode.svh"

module decoder (
    input           [6:0]   opcode_i,
    input           [4:0]   rd_i,
    input           [2:0]   fucnt3_i,
    input           [4:0]   rs1_i,
    input           [6:0]   funct7_i,
    // Regiser File control 
    output  logic           reg_write_o,
    // DMEM Read/Write Control
    output  logic   [3:0]   d_size_o,
    output  logic           d_unsigned_o,
    output  logic   [2:0]   mem_to_reg_o,
    output  logic           mem_read_o,
    output  logic           mem_write_o,
    // DMA enable signal
    output logic            dma_en_o
);

    // SIZES
    localparam SIZE_HALF = 2'b01;
    localparam SIZE_WORD = 2'b10;

    // REGISTER SOURCE
    localparam SRC_ALU = 3'b000;
    localparam SRC_DMEM = 3'b001;
    localparam SRC_PC_PLUS_4 = 3'b010;
    localparam SRC_IMM = 3'b011;
    localparam SRC_MUL = 3'b101;

    always_comb begin
        dma_en_o = '0;
        mem_read_o = '0;
        mem_write_o = '0;
        reg_write_o = '0;
        d_size_o = '0;
        d_unsigned_o = '0;
        mem_to_reg_o = '0;
        case (opcode_i)
            `OPCODE_R: begin
                reg_write_o = 1'b1;
                if (funct7_i == `FUNCT7_MULDIV) begin
                    mem_to_reg_o = SRC_MUL;         // M extension
                end else begin
                    mem_to_reg_o = SRC_ALU;         // arithmetic instructions
                end         
            end
            `OPCODE_I: begin
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_ALU;
            end
            `OPCODE_STORE: begin
                mem_write_o = 1'b1;
                case (fucnt3_i)
                    `FUNCT3_BYTE: begin
                        d_size_o = 4'b0001;
                    end
                    `FUNCT3_HALF: begin
                        d_size_o = 4'b0011;
                    end
                    `FUNCT3_WORD: begin
                        d_size_o = 4'b1111;
                    end
                    default: begin
                        d_size_o = '0;
                    end
                endcase
            end
            `OPCODE_LOAD: begin
                mem_read_o = 1'b1;
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_DMEM;
                case (fucnt3_i)
                    `FUNCT3_BYTE: begin
                        d_size_o = 4'b0001;
                    end
                    `FUNCT3_HALF: begin
                        d_size_o = 4'b0011;
                    end
                    `FUNCT3_WORD: begin
                        d_size_o = 4'b1111;
                    end
                    `FUNCT3_BYTE_U: begin
                        d_size_o = 4'b0001;
                        d_unsigned_o = 1'b1;
                    end
                    `FUNCT3_HALF_U: begin
                        d_size_o = 4'b0011;
                        d_unsigned_o = 1'b1;
                    end 
                    default: begin
                        d_size_o = '0;
                        d_unsigned_o = '0;
                    end
                endcase
            end
            `OPCODE_JALR: begin
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_PC_PLUS_4;
            end
            `OPCODE_JAL: begin
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_PC_PLUS_4;
            end
            `OPCODE_AUIPC: begin
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_ALU;
            end
            `OPCODE_LUI: begin
                reg_write_o = 1'b1;
                mem_to_reg_o = SRC_IMM;
            end
            `OPCODE_PIM: begin
                dma_en_o = 1'b1;
                mem_write_o = 1'b1;
            end
            default: begin
                dma_en_o = '0;
                mem_read_o = '0;
                mem_write_o = '0;
                reg_write_o = '0;
                d_size_o = '0;
                d_unsigned_o = '0;
                mem_to_reg_o = '0;
            end
        endcase
    end

endmodule