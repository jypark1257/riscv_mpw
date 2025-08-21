#include "ascii.h"
#include "string.h"
#include "uart.h"
#include "pim.h"

#define BUFFER_LEN 128

void dump_buffer(uint32_t source_addr, uint32_t size) {

    //if (source_addr % 4 != 0) {
    //    uwrite_int8s("Start address must be 4-byte aligned");
    //    uwrite_int8s("\n\r");
    //    return;
    //}

    //// Dump buffer out of range
    //if (source_addr + size > PIM_BUF_LIMIT) { 
    //    uwrite_int8s("Bump buffer out of range");
    //    uwrite_int8s("\n\r");
    //    return;
    //// Start address out of range
    //} else if ((source_addr < PIM_BUF_BASE) || (source_addr > PIM_BUF_LIMIT)) { 
    //    uwrite_int8s("Start address out of range");
    //    uwrite_int8s("\n\r");
    //    return;
    //} else {
    //    ;
    //}

    uint32_t *pim_buf = (uint32_t *)(source_addr);

    // DUMP 
    for (uint32_t idx = 0; idx < size; ++idx) {
        int8_t addr_buffer[BUFFER_LEN];
        int8_t data_buffer[BUFFER_LEN];
        volatile uint32_t data = pim_buf[idx];
        uwrite_int8s("buffer["); 
        uwrite_int8s(uint32_to_ascii_hex(((uint32_t)(idx)), addr_buffer, BUFFER_LEN));
        uwrite_int8s("]: ");
        uwrite_int8s(uint32_to_ascii_hex(data, data_buffer, BUFFER_LEN));
        uwrite_int8s("\n\r");
    }
    return;
}

void pim_erase(uint32_t pulse_width, uint8_t pulse_count, uint8_t row) {
    uint32_t width_count = (pulse_width << 5) | pulse_count;
    uint32_t row_col = (row << 9) | 0x0; // Column is not used in erase operation, set to 0
    asm volatile ( 
        "pim_erase %[a], 0(%[b])\n\t"
        :
        : [a] "r" (width_count), [b] "r" (row)
    );
    return;
}

void pim_program(uint32_t pulse_width, uint8_t pulse_count, uint8_t row, uint16_t col) {
    uint32_t width_count = (pulse_width << 5) | pulse_count;
    uint32_t row_col = (row << 9) | col;
    asm volatile (
        "pim_program %[a], 0(%[b])\n\t"
        :
        : [a] "r" (width_count), [b] "r" (row_col)
    );
    return;
}

void pim_zp(uint32_t zero_point) {
    asm volatile (
        "pim_zp %0, 0(%[a])\n\t"
        :
        : [a] "r" (zero_point)
    );
    return;
}

void pim_read (uint32_t buffer_addr, uint8_t row, uint16_t col) {
    uint32_t row_col = (row << 9) | col;
    asm volatile (
        "pim_read %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );
}

void pim_parallel(uint32_t buffer_addr, uint8_t row, uint16_t col) {
    uint32_t row_col = (row << 9) | col;
    asm volatile (
        "pim_parallel %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );
    return;
}
void pim_rbr(uint32_t buffer_addr, uint8_t row, uint16_t col) {
    uint32_t row_col = (row << 9) | col;
    asm volatile (
        "pim_rbr %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );
    return;
}

void pim_load (uint32_t buffer_addr, uint8_t compute_mode) {
    // compute mode
    // 1: parallel mode result
    // 2: rbr mode result
    asm volatile (
        "pim_load %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (compute_mode)
    );
}