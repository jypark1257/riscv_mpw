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
        uwrite_int8s("pim_buffer["); 
        uwrite_int8s(uint32_to_ascii_hex(((uint32_t)(idx)), addr_buffer, BUFFER_LEN));
        uwrite_int8s("]: ");
        uwrite_int8s(uint32_to_ascii_hex(data, data_buffer, BUFFER_LEN));
        uwrite_int8s("\n\r");
    }
    return;
}

//void pim_write(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//
//    asm volatile ( 
//        "pim_write %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//
//    //switch (sel_pim) {
//    //    case 1:
//    //        asm volatile ( 
//    //            "pim_write %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 2:
//    //        asm volatile ( 
//    //            "pim_write %[a], 2(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 3:
//    //        asm volatile ( 
//    //            "pim_write %[a], 3(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 4:
//    //        asm volatile ( 
//    //            "pim_write %[a], 4(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    default:
//    //        asm volatile ( 
//    //            "pim_write %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //}
//}
//
//void pim_compute(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//
//    asm volatile ( 
//        "pim_compute %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//
//    //switch (sel_pim) {
//    //    case 1:
//    //        asm volatile ( 
//    //            "pim_compute %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 2:
//    //        asm volatile ( 
//    //            "pim_compute %[a], 2(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 3:
//    //        asm volatile ( 
//    //            "pim_compute %[a], 3(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 4:
//    //        asm volatile ( 
//    //            "pim_compute %[a], 4(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    default:
//    //        asm volatile ( 
//    //            "pim_compute %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //}
//}
//
//void pim_load(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//    
//    asm volatile ( 
//        "pim_load %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//}
//
//void pim_key(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//
//    asm volatile ( 
//        "pim_key %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//
//    //switch (sel_pim) {
//    //    case 1:
//    //        asm volatile ( 
//    //            "pim_key %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 2:
//    //        asm volatile ( 
//    //            "pim_key %[a], 2(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 3:
//    //        asm volatile ( 
//    //            "pim_key %[a], 3(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    case 4:
//    //        asm volatile ( 
//    //            "pim_key %[a], 4(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //    default:
//    //        asm volatile ( 
//    //            "pim_key %[a], 1(%[b])\n\t"
//    //            :
//    //            : [a] "r" (source_addr), [b] "r" (size)
//    //        );
//    //        break;
//    //}
//}
//
//
//void pim_vref(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//
//    asm volatile ( 
//        "pim_vref %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//    return;
//}
//
//void pim_mode(uint32_t source_addr, uint8_t sel_pim, uint32_t size) {
//
//    asm volatile ( 
//        "pim_mode %[a], 0(%[b])\n\t"
//        :
//        : [a] "r" (source_addr), [b] "r" (size)
//    );
//    return;
//}