#include "types.h"

// 32KB
#define PIM_BUF_BASE ((volatile uint32_t)0x20000000)

/* PIM buffer functions */
void dump_buffer    (uint32_t source_addr, uint32_t size);

/* PIM functions */
void pim_erase      (uint32_t pulse_width, uint8_t pulse_count, uint8_t row);
void pim_program    (uint32_t pulse_width, uint8_t pulse_count, uint8_t row, uint16_t col);
void pim_zp         (uint32_t zero_point);
void pim_read       (uint32_t buffer_addr, uint8_t row, uint16_t col);
void pim_parallel   (uint32_t buffer_addr, uint8_t row, uint16_t col);
void pim_rbr        (uint32_t buffer_addr, uint8_t row, uint16_t col);
void pim_load       (uint32_t buffer_addr, uint8_t compute_mode);
