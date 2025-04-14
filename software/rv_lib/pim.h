#include "types.h"


#define PIM_BUF_BASE ((volatile uint32_t)0x20000000)
// 32KB
#define PIM_BUF_LIMIT ((volatile uint32_t)0x20008000)


/* PIM buffer functions */
void dump_buffer(uint32_t source_addr, uint32_t size);

/* PIM functions */
//void pim_write(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
//void pim_compute(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
//void pim_load(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
//void pim_key(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
//void pim_vref(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
//void pim_mode(uint32_t source_addr, uint8_t sel_pim, uint32_t size);
