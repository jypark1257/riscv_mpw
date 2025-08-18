OUTPUT_ARCH("riscv")

MEMORY {
    imem (rx)  : ORIGIN = 0x10000000, LENGTH = 0x00004000  /* 16KB */
    dmem (rwx) : ORIGIN = 0x10004000, LENGTH = 0x00004000  /* 16KB */ 
}

ENTRY(_start)

SECTIONS
{
    /* ---------- Code (IMEM) ---------- */
    .text.init : ALIGN(4)
    {
        *(.init)
    } > imem

    /* ---------- Read-Only Data (DMEM) ---------- */
    .rodata : ALIGN(4)
    {
        _srodata = .;
        *(.rodata)
        _erodata = .;
    } > dmem

    /* ---------- Initialized Data (DMEM) ---------- */
    .data : ALIGN(4)
    {
        PROVIDE(_global_pointer = . + 0x800);
        _sdata = .;
        *(.data)
        _edata = .;
    } > dmem

    /* ---------- Uninitialized Data (BSS) ---------- */
    .bss : ALIGN(4)
    {
        _sbss = .;
        *(.bss)
        _ebss = .;
    } > dmem

    /* ---------- Stack (Top of DMEM) ---------- */
    PROVIDE(_stack_pointer = ORIGIN(dmem) + LENGTH(dmem));
}
