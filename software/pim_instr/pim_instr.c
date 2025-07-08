


int main() {

    int width;  // 17-bit [21:5]
    int count;  // 5-bit [4:0]
    int width_count;
    volatile int buffer_addr;
    int row;    // 7-bit [15:9]
    int col;    // 9-bit [8:0]
    int row_col;
    int compute_mode;

    row_col = 0x0; // Initialize row_col to zero
    row = 0x1; 
    col = 0x1;
    row_col = (row << 9) | col; // Combine row and column into a single value

    width_count = 0x0;  // Initialize width_count to zero
    width = 0x1;
    count = 0x1;
    width_count = (width << 5) | count; // Combine width and count into

    asm volatile ( 
        "pim_erase %[a], 0(%[b])\n\t"
        :
        : [a] "r" (width_count), [b] "r" (row_col)
    );

    asm volatile (
        "pim_program %[a], 0(%[b])\n\t"
        :
        : [a] "r" (width_count), [b] "r" (row_col)
    );
    
    buffer_addr = 0x20000000;
    asm volatile (
        "pim_read %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );

    buffer_addr = 0x20000100;
    asm volatile (
        "pim_parallel %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );

    buffer_addr = 0x20000200;
    asm volatile (
        "pim_rbr %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (row_col)
    );

    buffer_addr = 0x20000300;
    compute_mode = 1; // parallel mode
    asm volatile (
        "pim_load %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (compute_mode)
    );

    buffer_addr = 0x20000400;
    compute_mode = 2; // rbr mode
    asm volatile (
        "pim_load %[a], 0(%[b])\n\t"
        :
        : [a] "r" (buffer_addr), [b] "r" (compute_mode)
    );

    while (1);

}