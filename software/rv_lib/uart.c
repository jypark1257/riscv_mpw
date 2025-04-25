#include "uart.h"

void uart_init(uint32_t clock_frequency, uint32_t baud_rate)
{
    // uint32_t symbol_edge_time = clock_frequency / baud_rate;
    // uint32_t sample_time = symbol_edge_time / 2;
    uint32_t symbol_edge_time = 5209; // clock_frequency / baud_rate;
    uint32_t sample_time = 2605; // symbol_edge_time / 2;
    UTRAN_SYMBOL_EDGE_TIME = symbol_edge_time;
    UTRAN_SAMPLE_TIME = sample_time;
}

void uwrite_int8(int8_t c)
{
    while (!UTRAN_CTRL) ;
    UTRAN_DATA = c;
}

void uwrite_int8s(const int8_t* s)
{
    for (int i = 0; s[i] != '\0'; i++) {
        uwrite_int8(s[i]);
    }
}

int8_t uread_int8(void)
{
    while (!URECV_CTRL) ;
    int8_t ch = URECV_DATA;
    if (ch == '\x0d') {
        uwrite_int8s("\r\n");
    } else {
        uwrite_int8(ch);
    }
    return ch;
}

int8_t *read_token(int8_t *b, uint32_t n, int8_t *ds)
{
    for (uint32_t i = 0; i < n; i++) {
        int8_t ch = uread_int8();
        for (uint32_t j = 0; ds[j] != '\0'; j++) {
            if (ch == ds[j]) {
                b[i] = '\0';
                return b;
            }
        }
        b[i] = ch;
    }
    b[n - 1] = '\0';
    return b;
}
