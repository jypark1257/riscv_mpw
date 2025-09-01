#include "ascii.h"
#include "uart.h"
#include "string.h"
#include "pim.h"

#define BUFFER_LEN 128

typedef void (*entry_t)(void);

int main(void) {
    // clock frequency: 100MHz
    // baud rate: 115200
    uart_init(25000000, 115200);

    // initialize buffer first (for debugging)
    (*((volatile uint32_t*)0x20000000)) = 0x12345678;
    (*((volatile uint32_t*)0x20000004)) = 0x9abcdef0;
    (*((volatile uint32_t*)0x20000008)) = 0xdeadbeef;
    (*((volatile uint32_t*)0x2000000c)) = 0xfacefeed;
    (*((volatile uint32_t*)0x20000010)) = 0x0badc0de;
    (*((volatile uint32_t*)0x20000014)) = 0x8badf00d;
    (*((volatile uint32_t*)0x20000018)) = 0xcafebabe;
    (*((volatile uint32_t*)0x2000001c)) = 0xfeedface;
    (*((volatile uint32_t*)0x20000020)) = 0xabad1dea;
    (*((volatile uint32_t*)0x20000024)) = 0xdeadbabe;
    (*((volatile uint32_t*)0x20000028)) = 0xfaceb00c;
    (*((volatile uint32_t*)0x2000002c)) = 0xdefec8ed;
    (*((volatile uint32_t*)0x20000030)) = 0xfee1dead;
    (*((volatile uint32_t*)0x20000034)) = 0xbaadf00d;
    (*((volatile uint32_t*)0x20000038)) = 0xdecafbad;
    (*((volatile uint32_t*)0x2000003c)) = 0xc001d00d;
    (*((volatile uint32_t*)0x20000040)) = 0x0defaced;
    (*((volatile uint32_t*)0x20000044)) = 0xdead10cc;
    (*((volatile uint32_t*)0x20000048)) = 0xfeedbabe;
    (*((volatile uint32_t*)0x2000004c)) = 0x8badf00d;
    (*((volatile uint32_t*)0x20000050)) = 0xcafed00d;
    (*((volatile uint32_t*)0x20000054)) = 0xdeadbeef;
    (*((volatile uint32_t*)0x20000058)) = 0xfacefeed;
    (*((volatile uint32_t*)0x2000005c)) = 0x0badc0de;
    (*((volatile uint32_t*)0x20000060)) = 0x8badf00d;
    (*((volatile uint32_t*)0x20000064)) = 0xcafebabe;
    (*((volatile uint32_t*)0x20000068)) = 0xfeedface;
    (*((volatile uint32_t*)0x2000006c)) = 0xabad1dea;
    (*((volatile uint32_t*)0x20000070)) = 0xdeadbabe;
    (*((volatile uint32_t*)0x20000074)) = 0xfaceb00c;
    (*((volatile uint32_t*)0x20000078)) = 0xdefec8ed;
    (*((volatile uint32_t*)0x2000007c)) = 0xfee1dead;
    (*((volatile uint32_t*)0x20000080)) = 0xbaadf00d;
    (*((volatile uint32_t*)0x20000084)) = 0xdecafbad;
    (*((volatile uint32_t*)0x20000088)) = 0xc001d00d;
    (*((volatile uint32_t*)0x2000008c)) = 0x0defaced;
    (*((volatile uint32_t*)0x20000090)) = 0xdead10cc;
    (*((volatile uint32_t*)0x20000094)) = 0xfeedbabe;
    (*((volatile uint32_t*)0x20000098)) = 0x8badf00d;
    (*((volatile uint32_t*)0x2000009c)) = 0xcafed00d;
    (*((volatile uint32_t*)0x200000a0)) = 0xdeadbeef;
    (*((volatile uint32_t*)0x200000a4)) = 0xfacefeed;
    (*((volatile uint32_t*)0x200000a8)) = 0x0badc0de;
    (*((volatile uint32_t*)0x200000ac)) = 0x8badf00d;   

    //(*((volatile uint32_t*)0x20000100))


    uwrite_int8s("\n\r");

    for ( ; ; ) {

        uwrite_int8s("RV_MPW> ");

        int8_t buf_command[BUFFER_LEN];
        int8_t buf_pulse_width[BUFFER_LEN];
        int8_t buf_pulse_count[BUFFER_LEN];
        int8_t buf_row[BUFFER_LEN];
        int8_t buf_col[BUFFER_LEN];
        int8_t buf_zero_point[BUFFER_LEN];
        int8_t buf_buffer_addr[BUFFER_LEN];
        int8_t buf_size[BUFFER_LEN];

        int8_t *input = read_token(buf_command, BUFFER_LEN, " \x0d");

        if (strcmp(input, "pim_erase") == 0) {
            /* Instruction parsing */
            int8_t *str_pulse_width = read_token(buf_pulse_width, BUFFER_LEN, " \x0d");
            int8_t *str_pulse_count = read_token(buf_pulse_count, BUFFER_LEN, " \x0d");
            int8_t *str_row = read_token(buf_row, BUFFER_LEN, " \x0d");
            uint32_t pulse_width = ascii_dec_to_uint32(str_pulse_width);
            uint8_t pulse_count = (uint8_t)ascii_dec_to_uint32(str_pulse_count);
            uint8_t row = (uint8_t)ascii_dec_to_uint32(str_row);
            pim_erase(pulse_width, pulse_count, row);

        } else if (strcmp(input, "pim_program") == 0) {
            /* Instruction parsing */
            int8_t *str_pulse_width = read_token(buf_pulse_width, BUFFER_LEN, " \x0d");
            int8_t *str_pulse_count = read_token(buf_pulse_count, BUFFER_LEN, " \x0d");
            int8_t *str_row = read_token(buf_row, BUFFER_LEN, " \x0d");
            int8_t *str_col = read_token(buf_col, BUFFER_LEN, " \x0d");
            uint32_t pulse_width = ascii_dec_to_uint32(str_pulse_width);
            uint8_t pulse_count = (uint8_t)ascii_dec_to_uint32(str_pulse_count);
            uint8_t row = (uint8_t)ascii_dec_to_uint32(str_row);
            uint16_t col = (uint16_t)ascii_dec_to_uint32(str_col);
            pim_program(pulse_width, pulse_count, row, col);

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
            //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "pim_zp") == 0) {
            /* Instruction parsing */
            int8_t *str_zero_point = read_token(buf_zero_point, BUFFER_LEN, " \x0d");
            uint32_t zero_point = ascii_dec_to_uint32(str_zero_point);
            pim_zp(zero_point);

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
            //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "pim_read") == 0) {
            /* Instruction parsing */
            int8_t *str_buffer_addr = read_token(buf_buffer_addr, BUFFER_LEN, " \x0d");
            int8_t *str_row = read_token(buf_row, BUFFER_LEN, " \x0d");
            int8_t *str_col = read_token(buf_col, BUFFER_LEN, " \x0d");
            uint32_t buffer_addr = ascii_hex_to_uint32(str_buffer_addr);
            uint8_t row = (uint8_t)ascii_dec_to_uint32(str_row);
            uint16_t col = (uint16_t)ascii_dec_to_uint32(str_col);
            pim_read(buffer_addr, row, col);    

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
            //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "pim_parallel") == 0) {
            /* Instruction parsing */
            int8_t *str_buffer_addr = read_token(buf_buffer_addr, BUFFER_LEN, " \x0d");
            int8_t *str_row = read_token(buf_row, BUFFER_LEN, " \x0d");
            int8_t *str_col = read_token(buf_col, BUFFER_LEN, " \x0d");
            uint32_t buffer_addr = ascii_hex_to_uint32(str_buffer_addr);
            uint8_t row = (uint8_t)ascii_dec_to_uint32(str_row);
            uint16_t col = (uint16_t)ascii_dec_to_uint32(str_col);
            pim_parallel(buffer_addr, row, col);    

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
            //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "pim_rbr") == 0) {
            /* Instruction parsing */
            int8_t *str_buffer_addr = read_token(buf_buffer_addr, BUFFER_LEN, " \x0d");
            int8_t *str_row = read_token(buf_row, BUFFER_LEN, " \x0d");
            int8_t *str_col = read_token(buf_col, BUFFER_LEN, " \x0d");
            uint32_t buffer_addr = ascii_hex_to_uint32(str_buffer_addr);
            uint8_t row = (uint8_t)ascii_dec_to_uint32(str_row);
            uint16_t col = (uint16_t)ascii_dec_to_uint32(str_col);
            pim_rbr(buffer_addr, row, col);

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
            //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "pim_load") == 0) {
            /* Instruction parsing */
            int8_t *str_buffer_addr = read_token(buf_buffer_addr, BUFFER_LEN, " \x0d");
            int8_t *str_compute_mode = read_token(buf_row, BUFFER_LEN, " \x0d");
            uint32_t buffer_addr = ascii_hex_to_uint32(str_buffer_addr);
            uint8_t compute_mode = (uint8_t)ascii_dec_to_uint32(str_compute_mode);
            pim_load(buffer_addr, compute_mode);

            /* print parameter */
            //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(buffer_addr, str_buffer_addr, BUFFER_LEN)); 
            //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(compute_mode, str_compute_mode, BUFFER_LEN)); uwrite_int8s(")");
            //uwrite_int8s("\n\r");
        } else if (strcmp(input, "dump") == 0) {
            /* Instruction parsing */
            int8_t *str_buffer_addr = read_token(buf_buffer_addr, BUFFER_LEN, " \x0d");
            int8_t *str_size = read_token(buf_size, BUFFER_LEN, " \x0d");
            uint32_t buffer_addr = ascii_hex_to_uint32(str_buffer_addr);
            uint32_t size = ascii_dec_to_uint32(str_size);
            dump_buffer(buffer_addr, size);

        } else if (strcmp(input, "help") == 0) {
            uwrite_int8s("Please ask jiyong, jiyong is the best!!");
            uwrite_int8s("\n\r");

        } else {
            uwrite_int8s("Unrecognized token: ");
            uwrite_int8s(input);
            uwrite_int8s("\n\r");

        }
    }

    while (1);

    return 0;
}
