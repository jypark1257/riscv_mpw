OUTPUT_ARCH("riscv")

MEMORY {
    imem (rx)  : ORIGIN = 0x10000000, LENGTH = 0x00001000
    dmem (rwx) : ORIGIN = 0x10001000, LENGTH = 0x00001000
}

ENTRY(_start)

SECTIONS
{
    /* IMEM */
    . = 0x10000000;
    .text.init :
    {
        *(.init)
    } > imem

    /* DMEM */
    . = 0x10001000;
    .rodata :
    {
        _srodata = .;
        *(.rodata)
        _erodata = .;
    } > dmem

    . = ALIGN(4); /* rodata 끝난 후 4바이트 정렬 */
    .data :
    {
        PROVIDE(_global_pointer = . + 0x800);
        _sdata = .;
        *(.data)
        _edata = .;
    } > dmem

    .bss :
    {
        _sbss = .;
        *(.bss)
        _ebss = .;
    } > dmem

    /* Stack Pointer - End of DMEM */
    PROVIDE(_stack_pointer = ORIGIN(dmem) + LENGTH(dmem));
}
