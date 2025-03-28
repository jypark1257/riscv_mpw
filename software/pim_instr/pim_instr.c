
#define DMA_CTRL (*((volatile unsigned int*)0x10000000) & 0x01)

int main() {

    int source;
    int weight_size;
    int act_size;
    int result_size;
    act_size = 72;
    result_size = 256;

    
    weight_size = 4608;
    source = 0x20000000;
    asm volatile ( 
        "pim_write %[a], 1(%[b])\n\t"
        :
        : [a] "r" (source), [b] "r" (weight_size)
    );
    asm volatile ( 
        "pim_compute %[a], 1(%[b])\n\t"
        :
        : [a] "r" (source), [b] "r" (act_size)
    );
    asm volatile ( 
        "pim_load %[a], 1(%[b])\n\t"
        :
        : [a] "r" (source), [b] "r" (result_size)
    );
    asm volatile ( 
        "pim_key %[a], 1(%[b])\n\t"
        :
        : [a] "r" (source), [b] "r" (result_size)
    );

    while (1);

}