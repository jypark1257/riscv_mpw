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

    dut.rst_ni.value = 0

    # Create a 10ns period clock on port clk
    clock = Clock(dut.clk_i, 10, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))



    await Timer(1, units="ns")
    dut.rst_ni.value = 1
    dut.clear_i.value = 0
    dut.in_addr_i.value = 0
    dut.in_instr_i.value = 0
    dut.in_valid_i.value = 0


    for _ in range(10):
        await FallingEdge(dut.clk_i)
        dut.in_addr_i.value = random.randrange(0, 2**32)
        dut.in_instr_i.value = random.randrange(0, 2**32)
        dut.in_valid_i.value = 1
        await RisingEdge(dut.clk_i)
        await Timer(1, units="ns")
        dut.in_valid_i.value = 0
    
    for _ in range(10):
        await FallingEdge(dut.clk_i)
        dut.clear_i.value = 1
        await RisingEdge(dut.clk_i)
        await Timer(1, units="ns")
        dut.clear_i.value = 0

 
    for _ in range(10):
        await FallingEdge(dut.clk_i)
        dut.in_addr_i.value = random.randrange(0, 2**32)
        dut.in_instr_i.value = random.randrange(0, 2**32)
        dut.in_valid_i.value = 1
        await RisingEdge(dut.clk_i)
        await Timer(1, units="ns")
        dut.in_valid_i.value = 0