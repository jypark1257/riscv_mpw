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


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def rvtest_add(dut):

    dut.rv_rst_ni.value = 0

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    await Timer(1, units="ns")
    
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # program initialization for 4x sram_4096w_8b
    imem_path = "../../software/asm_tests/add.hex"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        await RisingEdge(dut.clk_i)
        
    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"


@cocotb.test()
async def rvtest_sub(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sub.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

    

@cocotb.test()
async def rvtest_xor(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/xor.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_or(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/or.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_and(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/and.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sll(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sll.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_srl(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/srl.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_slt(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/slt.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sltu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sltu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_addi(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/addi.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_xori(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/xori.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_ori(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/ori.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_andi(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/andi.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_slli(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/slli.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_srli(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/srli.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_srai(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/srai.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_slti(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/slti.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sltiu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sltiu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lb(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lb.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1

    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lh(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lh.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lw(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lw.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lbu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lbu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lhu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lhu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sb(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sb.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sh(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sh.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_sw(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/sw.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_beq(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/beq.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_bne(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/bne.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_blt(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/blt.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_bge(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/bge.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_bltu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/bltu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_bgeu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/bgeu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_jal(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/jal.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_jalr(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/jalr.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_lui(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/lui.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_auipc(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/auipc.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"


# M extenstion assembly test

@cocotb.test()
async def rvtest_mul(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/mul.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_mulh(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/mulh.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_mulhsu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/mulhsu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_mulhu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/mulhu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_div(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/div.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_divu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/divu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_rem(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/rem.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"

@cocotb.test()
async def rvtest_remu(dut):

    
    dut.rv_rst_ni.value = 0
    # memory initialization
    imem_path = "../../software/asm_tests/remu.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    # sram_4096w_8b 메모리 초기화 (512 rows x 64 bits)
    for idx in range (0, 512):
        dut.genblk1.M0_0.mem[idx].value = 0
        dut.genblk1.M0_1.mem[idx].value = 0
        dut.genblk1.M0_2.mem[idx].value = 0
        dut.genblk1.M0_3.mem[idx].value = 0
    for idx in range (0, 512):
        dut.genblk1.M1_0.mem[idx].value = 0
    await Timer(1, units="ns")

    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            # sram_4096w_8b 어드레싱: MUX=8 (3-bit), 512 rows
            mux_addr = idx & 0x00000007     # 3-bit (0-7)
            row_addr = (idx >> 3) & 0x1ff   # 9-bit (0-511)
            if idx < 4096:
                # instruction memory (idx < 4096)
                data0 =  dut.genblk1.M0_0.mem[row_addr].value
                data1 =  dut.genblk1.M0_1.mem[row_addr].value
                data2 =  dut.genblk1.M0_2.mem[row_addr].value
                data3 =  dut.genblk1.M0_3.mem[row_addr].value

                # 32비트를 4개의 8비트 SRAM에 분산 저장 (sram_4096w_8b 구조에 맞게)
                data0 = data0 | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                data0 = data0 | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))

                data1 = data1 | (((inst_decimal & 0x00000100) >> 8)  << (0*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000200) >> 9)  << (1*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000400) >> 10) << (2*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00000800) >> 11) << (3*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00001000) >> 12) << (4*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00002000) >> 13) << (5*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00004000) >> 14) << (6*8 + mux_addr))
                data1 = data1 | (((inst_decimal & 0x00008000) >> 15) << (7*8 + mux_addr))

                data2 = data2 | (((inst_decimal & 0x00010000) >> 16) << (0*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00020000) >> 17) << (1*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00040000) >> 18) << (2*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00080000) >> 19) << (3*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00100000) >> 20) << (4*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00200000) >> 21) << (5*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00400000) >> 22) << (6*8 + mux_addr))
                data2 = data2 | (((inst_decimal & 0x00800000) >> 23) << (7*8 + mux_addr))

                data3 = data3 | (((inst_decimal & 0x01000000) >> 24) << (0*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x02000000) >> 25) << (1*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x04000000) >> 26) << (2*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x08000000) >> 27) << (3*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x10000000) >> 28) << (4*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x20000000) >> 29) << (5*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x40000000) >> 30) << (6*8 + mux_addr))
                data3 = data3 | (((inst_decimal & 0x80000000) >> 31) << (7*8 + mux_addr))

                dut.genblk1.M0_0.mem[row_addr].value = data0
                dut.genblk1.M0_1.mem[row_addr].value = data1
                dut.genblk1.M0_2.mem[row_addr].value = data2
                dut.genblk1.M0_3.mem[row_addr].value = data3
            else: 
                # data memory 처리 (4096 이상)
                ddata = dut.genblk1.M1_0.mem[row_addr].value
                ddata = ddata | (((inst_decimal & 0x00000001) >> 0)  << (0*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000002) >> 1)  << (1*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000004) >> 2)  << (2*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000008) >> 3)  << (3*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000010) >> 4)  << (4*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000020) >> 5)  << (5*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000040) >> 6)  << (6*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000080) >> 7)  << (7*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000100) >> 8)  << (8*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000200) >> 9)  << (9*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000400) >> 10) << (10*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00000800) >> 11) << (11*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00001000) >> 12) << (12*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00002000) >> 13) << (13*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00004000) >> 14) << (14*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00008000) >> 15) << (15*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00010000) >> 16) << (16*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00020000) >> 17) << (17*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00040000) >> 18) << (18*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00080000) >> 19) << (19*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00100000) >> 20) << (20*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00200000) >> 21) << (21*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00400000) >> 22) << (22*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x00800000) >> 23) << (23*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x01000000) >> 24) << (24*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x02000000) >> 25) << (25*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x04000000) >> 26) << (26*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x08000000) >> 27) << (27*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x10000000) >> 28) << (28*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x20000000) >> 29) << (29*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x40000000) >> 30) << (30*8 + mux_addr))
                ddata = ddata | (((inst_decimal & 0x80000000) >> 31) << (31*8 + mux_addr))
                dut.genblk1.M1_0.mem[row_addr].value = ddata
            
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(1000):
        
        await RisingEdge(dut.clk_i)

    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"