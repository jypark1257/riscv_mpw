// Pipe reg: IF/ID
typedef struct packed {
    logic   [31:0]  pc;
    logic   [31:0]  instr;
} pipe_if_id;

// Pipe reg: ID/EX
typedef struct packed {
    logic   [31:0]  pc;
    logic   [6:0]   opcode;
    logic   [4:0]   rd;         // rd for regfile
    logic   [2:0]   funct3;
    logic   [4:0]   rs1;
    logic   [4:0]   rs2;
    logic   [6:0]   funct7;
    logic   [31:0]  imm;
    logic           mem_read;
    logic           mem_write;
    logic           reg_write;
    logic   [2:0]   mem_to_reg;
    logic   [3:0]   d_size;
    logic           d_unsigned;
    logic           dma_en;
    logic   [31:0]  rs1_dout;
    logic   [31:0]  rs2_dout;
} pipe_id_ex;

// Pipe reg: MEM/WB
typedef struct packed {
    logic   [31:0]  pc_plus_4;
    logic   [4:0]   rd;
    logic   [31:0]  imm;
    logic   [31:0]  alu_result;
    logic   [31:0]  mul_result;     // M extension
    logic           reg_write;
    logic   [2:0]   mem_to_reg;
    logic   [3:0]   d_size;
    logic           d_unsigned;
} pipe_ex_wb;