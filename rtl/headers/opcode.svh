// OPCODES 
`define OPCODE_R            7'b0110011
`define OPCODE_I            7'b0010011
`define OPCODE_BRANCH       7'b1100011
`define OPCODE_STORE        7'b0100011
`define OPCODE_LOAD         7'b0000011
`define OPCODE_JALR         7'b1100111
`define OPCODE_JAL          7'b1101111
`define OPCODE_AUIPC        7'b0010111
`define OPCODE_LUI          7'b0110111
`define OPCODE_SYSTEM       7'b1110011    // CSRXX, ECALL (NOT IMPLEMENTED), EBREAK (NOT IMPLEMENTED)
`define OPCODE_PIM          7'b0001011
`define OPCODE_CUSTON_1     7'b0101011
`define OPCODE_CUSTON_2     7'b1011011  // custom / rv128
`define OPCODE_CUSTON_3     7'b1111011  // custom / rv128

// FUNCT3 (ALU)
`define FUNCT3_ADD_SUB      3'b000
`define FUNCT3_SLL          3'b001
`define FUNCT3_SLT          3'b010
`define FUNCT3_SLTU         3'b011
`define FUNCT3_XOR          3'b100
`define FUNCT3_SRL_SRA      3'b101
`define FUNCT3_OR           3'b110
`define FUNCT3_AND          3'b111

// FUNCT3 (BRANCH)
`define BRANCH_BEQ          3'b000
`define BRANCH_BNE          3'b001
`define BRANCH_BLT          3'b100
`define BRANCH_BGE          3'b101
`define BRANCH_BLTU         3'b110
`define BRANCH_BGEU         3'b111

// FUNCT3 (MUL/DIV)
`define FUNCT3_MUL          3'b000
`define FUNCT3_MULH         3'b001
`define FUNCT3_MULHSU       3'b010  
`define FUNCT3_MULHU        3'b011
`define FUNCT3_DIV          3'b100
`define FUNCT3_DIVU         3'b101
`define FUNCT3_REM          3'b110
`define FUNCT3_REMU         3'b111

// FUNCT7 (MUL/DIV)
`define FUNCT7_MULDIV          7'h01

// SIGNED LOAD, STORE
`define FUNCT3_BYTE         3'b000
`define FUNCT3_HALF         3'b001
`define FUNCT3_WORD         3'b010

// UNSIGNED LOAD FUNCT3
`define FUNCT3_BYTE_U       3'b100
`define FUNCT3_HALF_U       3'b101




