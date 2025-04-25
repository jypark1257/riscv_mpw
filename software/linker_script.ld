OUTPUT_ARCH( "riscv" )

MEMORY {
    imem  (rwx): ORIGIN = 0x10000000, LENGTH = 0x00001000
    dmem  (rwx): ORIGIN = 0x10001000, LENGTH = 0x00001000
}

ENTRY(_start)
SECTIONS
{
    /* IMEM */
    . = 0x10000000;
    /* gp is set to start of memory for gp relative addressing of static vars*/
    /* gp start is ram origin + 0x800 --- because offset for load/store is 12b */
    /* 12b signed = -2048 to +2047 */
    .text.init : 
    { 
        *(.init)
    } > imem

    /* DMEM */
    .rodata  :
    {
        _srodata = .;
        *(.rodata)
        _erodata = .;
    } > dmem
    .data 0x10001100:
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
    /* Stack Pointer - End of Memory */
    .stack :
    {
        PROVIDE(_stack_pointer = ORIGIN(dmem) + LENGTH(dmem));
        _sstack = .;
        *(.stack)
        _estack = .;
    } > dmem
}
