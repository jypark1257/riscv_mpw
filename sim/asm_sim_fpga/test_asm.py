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
async def rvtest_add(dut):

    dut.rv_rst_ni.value = 0

    imem_path = "../../software/asm_tests/rvc.hex"

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)
    await Timer(1, units="ns")
    for idx in range (0, 1024*4):
        dut.genblk1.imem_0.imem_sram.d0[idx]
        dut.genblk1.imem_0.imem_sram.d1[idx]
        dut.genblk1.imem_0.imem_sram.d2[idx]
        dut.genblk1.imem_0.imem_sram.d3[idx]
    for idx in range (0, 1024*4):
        dut.genblk1.dmem_0.dmem_sram.d0[idx]
        dut.genblk1.dmem_0.dmem_sram.d1[idx]
        dut.genblk1.dmem_0.dmem_sram.d2[idx]
        dut.genblk1.dmem_0.dmem_sram.d3[idx]
    await Timer(1, units="ns")

    # program initialization for 4x sram_4096w_8b
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            if idx < (1024*4):
                data0 = ((inst_decimal & 0x000000FF) >> 0)
                data1 = ((inst_decimal & 0x0000FF00) >> 8)
                data2 = ((inst_decimal & 0x00FF0000) >> 16)
                data3 = ((inst_decimal & 0xFF000000) >> 24)
                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
            else:
                data0 = ((inst_decimal & 0x000000FF) >> 0)
                data1 = ((inst_decimal & 0x0000FF00) >> 8)
                data2 = ((inst_decimal & 0x00FF0000) >> 16)
                data3 = ((inst_decimal & 0xFF000000) >> 24)
                dut.genblk1.dmem_0.dmem_sram.d0[idx-(1024*4)].value = data0
                dut.genblk1.dmem_0.dmem_sram.d1[idx-(1024*4)].value = data1
                dut.genblk1.dmem_0.dmem_sram.d2[idx-(1024*4)].value = data2
                dut.genblk1.dmem_0.dmem_sram.d3[idx-(1024*4)].value = data3
            await RisingEdge(dut.clk_i)
            idx = idx + 1
    
    await Timer(1, units="ns")
    dut.rv_rst_ni.value = 1

    for _ in range(10000):
        await RisingEdge(dut.clk_i)
    
    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"


#@cocotb.test()
#async def rvtest_sub(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sub.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#    
#
#@cocotb.test()
#async def rvtest_xor(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/xor.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_or(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/or.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_and(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/and.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sll(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sll.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_srl(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/srl.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_slt(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/slt.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sltu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sltu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_addi(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/addi.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_xori(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/xori.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_ori(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/ori.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_andi(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/andi.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_slli(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/slli.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_srli(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/srli.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_srai(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/srai.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_slti(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/slti.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sltiu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sltiu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lb(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lb.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lh(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lh.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lw(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lw.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lbu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lbu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lhu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lhu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sb(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sb.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sh(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sh.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_sw(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/sw.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_beq(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/beq.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_bne(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/bne.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_blt(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/blt.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_bge(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/bge.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_bltu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/bltu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_bgeu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/bgeu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_jal(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/jal.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_jalr(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/jalr.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_lui(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/lui.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_auipc(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/auipc.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#
## M extenstion assembly test
#
#@cocotb.test()
#async def rvtest_mul(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/mul.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_mulh(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/mulh.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_mulhsu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/mulhsu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_mulhu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/mulhu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_div(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/div.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_divu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/divu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_rem(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/rem.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"
#
#@cocotb.test()
#async def rvtest_remu(dut):
#
#    
#    dut.rv_rst_ni.value = 0
#    # memory initialization
#    imem_path = "../../software/asm_tests/remu.hex"
#
#    # Create a 10ns period clock on port clk
#    clock = Clock(dut.clk_i, 10, units="ns")  
#    # Start the clock. Start it low to avoid issues on the first RisingEdge
#    cocotb.start_soon(clock.start(start_high=False))
#
#    await RisingEdge(dut.clk_i)
#    await Timer(1, units="ns")
#    for idx in range (0, 1024):
#        dut.genblk1.imem_0.imem_sram.d0[idx]
#        dut.genblk1.imem_0.imem_sram.d1[idx]
#        dut.genblk1.imem_0.imem_sram.d2[idx]
#        dut.genblk1.imem_0.imem_sram.d3[idx]
#    for idx in range (0, 1024):
#        dut.genblk1.dmem_0.dmem_sram.d0[idx]
#        dut.genblk1.dmem_0.dmem_sram.d1[idx]
#        dut.genblk1.dmem_0.dmem_sram.d2[idx]
#        dut.genblk1.dmem_0.dmem_sram.d3[idx]
#    await Timer(1, units="ns")
#
#    # program initialization for 4x sram_4096w_8b
#    with open(imem_path, "r") as mem:
#        first_line = mem.readline()
#        idx  = 0
#        for line in mem:
#            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
#            inst_decimal = int(inst, 16)
#            if idx < 1024:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.imem_0.imem_sram.d0[idx].value = data0
#                dut.genblk1.imem_0.imem_sram.d1[idx].value = data1
#                dut.genblk1.imem_0.imem_sram.d2[idx].value = data2
#                dut.genblk1.imem_0.imem_sram.d3[idx].value = data3
#            else:
#                data0 = ((inst_decimal & 0x000000FF) >> 0)
#                data1 = ((inst_decimal & 0x0000FF00) >> 8)
#                data2 = ((inst_decimal & 0x00FF0000) >> 16)
#                data3 = ((inst_decimal & 0xFF000000) >> 24)
#                dut.genblk1.dmem_0.dmem_sram.d0[idx-1024].value = data0
#                dut.genblk1.dmem_0.dmem_sram.d1[idx-1024].value = data1
#                dut.genblk1.dmem_0.dmem_sram.d2[idx-1024].value = data2
#                dut.genblk1.dmem_0.dmem_sram.d3[idx-1024].value = data3
#            await RisingEdge(dut.clk_i)
#            idx = idx + 1
#
#    await Timer(1, units="ns")
#    dut.rv_rst_ni.value = 1
#
#    for _ in range(1000):
#        
#        await RisingEdge(dut.clk_i)
#
#    assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"