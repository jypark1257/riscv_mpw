# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# test_my_design.py (simple)

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb.triggers import Timer
from cocotb.types import LogicArray


@cocotb.test()
async def rvtest_uart(dut):

    dut.rv_rst_ni.value = 0
    dut.spi_rst_ni.value = 0

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    await Timer(1, units="ns")
    for idx in range (0, 256):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 256):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # program initialization for 4x sram_4096w_8b
    imem_path = "../../software/bios/bios.hex"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            mux_addr = idx & 0x00000003     # 2-bit
            row_addr = (idx & 0x000003fc) >> 2     # 8-bit
            if idx < 1024:
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << ( 0*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << ( 1*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << ( 2*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << ( 3*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << ( 4*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << ( 5*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << ( 6*4  + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << ( 7*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << ( 0*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << ( 1*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << ( 2*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << ( 3*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << ( 4*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << ( 5*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << ( 6*4  + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << ( 7*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << ( 0*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << ( 1*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << ( 2*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << ( 3*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << ( 4*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << ( 5*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << ( 6*4  + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << ( 7*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << ( 0*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << ( 1*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << ( 2*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << ( 3*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << ( 4*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << ( 5*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << ( 6*4  + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << ( 7*4  + mux_addr))
                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else:
                ddata =  dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << ( 0*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << ( 1*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << ( 2*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << ( 3*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << ( 4*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << ( 5*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << ( 6*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << ( 7*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << ( 8*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << ( 9*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*4  + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*4  + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(10000):
        await RisingEdge(dut.clk_i)
        
