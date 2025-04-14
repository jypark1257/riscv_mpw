#include "ascii.h"
#include "uart.h"
#include "string.h"
//#include "pim.h"

#define BUFFER_LEN 128

typedef void (*entry_t)(void);

int main(void)
{
    uart_init(25000000, 9600);

    uwrite_int8s("\n\r");

    for ( ; ; ) {
        uwrite_int8s("RV_MPW> ");

        int8_t buffer[BUFFER_LEN];
        int8_t sel_pim[BUFFER_LEN];
        int8_t size[BUFFER_LEN];
        int8_t *input = read_token(buffer, BUFFER_LEN, " \x0d");

        //if (strcmp(input, "pim_write") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    pim_write(source_addr, sel_pim, size);
//
        //    /* print parameter */
        //    //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
        //    //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
        //    //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
        //    //uwrite_int8s("\n\r");
        //} else if (strcmp(input, "pim_compute") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    pim_compute(source_addr, sel_pim, size);
//
        //    /* print parameter */
        //    //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
        //    //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
        //    //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
        //    //uwrite_int8s("\n\r");
        //} else if (strcmp(input, "pim_load") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    pim_load(source_addr, sel_pim, size);
//
        //    /* print parameter */
        //    //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
        //    //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
        //    //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
        //    //uwrite_int8s("\n\r");
        //} else if (strcmp(input, "pim_key") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    pim_key(source_addr, sel_pim, size);
//
        //    /* print parameter */
        //    //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
        //    //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
        //    //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
        //    //uwrite_int8s("\n\r");
        //} else if (strcmp(input, "pim_mode") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    pim_mode(source_addr, sel_pim, size);
//
        //    /* print parameter */
        //    //uwrite_int8s("pim_write "); uwrite_int8s(uint32_to_ascii_hex(source_addr, str_source_addr, BUFFER_LEN)); 
        //    //uwrite_int8s(", "); uwrite_int8s(uint8_to_ascii_hex(sel_pim, str_sel_pim, BUFFER_LEN)); 
        //    //uwrite_int8s("("); uwrite_int8s(uint32_to_ascii_hex(size, str_size, BUFFER_LEN)); uwrite_int8s(")");
        //    //uwrite_int8s("\n\r");
        //} else if (strcmp(input, "dump") == 0) {
        //    /* Instruction parsing */
        //    int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
        //    int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
        //    uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
        //    uint32_t size = ascii_dec_to_uint32(str_size);
        //    dump_buffer(source_addr, size);
        if (strcmp(input, "help") == 0) {
            uwrite_int8s("Please ask jiyong, jiyong is the best!!");
            uwrite_int8s("\n\r");
        } //else if (strcmp(input, "pim_vref") == 0) {
          //  int8_t *str_source_addr = read_token(buffer, BUFFER_LEN, " \x0d");
          //  int8_t *str_sel_pim = read_token(sel_pim, BUFFER_LEN, " \x0d");
          //  int8_t *str_size = read_token(size, BUFFER_LEN, " \x0d");
          //  uint32_t source_addr = ascii_hex_to_uint32(str_source_addr);
          //  uint8_t sel_pim = ascii_dec_to_uint8(str_sel_pim);
          //  uint32_t size = ascii_dec_to_uint32(str_size);
          //  pim_vref(source_addr, sel_pim, size);
        else {
            uwrite_int8s("Unrecognized token: ");
            uwrite_int8s(input);
            uwrite_int8s("\n\r");
        }
    }

    while (1);

    return 0;
}


