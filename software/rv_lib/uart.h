#ifndef UART_H_
#define UART_H_

#include "types.h"

#define URECV_CTRL              (*((volatile uint32_t*)0x80000000) & 0x02)
#define URECV_DATA              (*((volatile uint32_t*)0x80000004) & 0xff)
#define UTRAN_CTRL              (*((volatile uint32_t*)0x80000000) & 0x01)
#define UTRAN_DATA              (*((volatile uint32_t*)0x80000008))
#define UTRAN_SYMBOL_EDGE_TIME  (*((volatile uint32_t*)0x8000000C))
#define UTRAN_SAMPLE_TIME       (*((volatile uint32_t*)0x80000010))

void uart_init(uint32_t clock_frequency, uint32_t baud_rate);
void uwrite_int8(int8_t c);
void uwrite_int8s(const int8_t* s);
int8_t uread_int8(void);
int8_t *read_token(int8_t *b, uint32_t n, int8_t *ds);

#endif
