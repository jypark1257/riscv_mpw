#include "ascii.h"
#include "uart.h"
#include "string.h"

#define BUFFER_LEN 128

typedef void (*entry_t)(void);

int main(void)
{
    // clock frequency: 100MHz
    // baud rate: 115200
    uart_init(100000000, 115200);

    uwrite_int8s("\n\r");

    for ( ; ; ) {
        uwrite_int8s("RV_MPW> ");

        int8_t buffer[BUFFER_LEN];
        int8_t sel_pim[BUFFER_LEN];
        int8_t size[BUFFER_LEN];
        int8_t *input = read_token(buffer, BUFFER_LEN, " \x0d");

        if (strcmp(input, "help") == 0) {
            uwrite_int8s("Please ask jiyong, jiyong is the best!!");
            uwrite_int8s("\n\r");
        }  else {
            uwrite_int8s("Unrecognized token: ");
            uwrite_int8s(input);
            uwrite_int8s("\n\r");
        }
    }

    while (1);

    return 0;
}


