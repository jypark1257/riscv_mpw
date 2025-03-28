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
import asyncio
from cocotbext.spi import *

async def write_sram(dut, spi_master, address, data):
    addr_0 = (address & 0xFF)
    addr_1 = (address & 0xFF00) >> 8
    addr_2 = (address & 0xFF0000) >> 16
    addr_3 = (address & 0xFF000000) >> 24
    data_0 = (data & 0xFF)
    data_1 = (data & 0xFF00) >> 8
    data_2 = (data & 0xFF0000) >> 16
    data_3 = (data & 0xFF000000) >> 24

    # address
    await spi_master.write([0x01])  # command
    await Timer(3, units="ns")
    await spi_master.write([addr_3])
    await Timer(3, units="ns")
    await spi_master.write([addr_2])
    await Timer(3, units="ns")
    await spi_master.write([addr_1])
    await Timer(3, units="ns")
    await spi_master.write([addr_0])
    await Timer(3, units="ns")
    # data
    await spi_master.write([0x02])  # command
    await Timer(3, units="ns")
    await spi_master.write([data_3])
    await Timer(3, units="ns")
    await spi_master.write([data_2])
    await Timer(3, units="ns")
    await spi_master.write([data_1])
    await Timer(3, units="ns")
    await spi_master.write([data_0])
    await Timer(3, units="ns")


@cocotb.test()
async def core_bench(dut):

    imem_path = "../../software/pim_instr_test/pim_instr.hex"

    dut.i_rv_rst_n.value = 0
    dut.i_spi_rst_n.value = 0

    # Create a 10ns period clock on port clk
    clock = Clock(dut.i_clk, 4, units="ns")  
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    # spi master
    spi_bus = SpiBus.from_entity(dut)
    spi_config = SpiConfig(
        word_width      = 8,
        sclk_freq       = 25e6,
        cpol            = False,
        cpha            = False,
        msb_first       = True,
        cs_active_low   = True
    )
    spi_master = SpiMaster(spi_bus, spi_config)

    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    for idx in range (0, 256):
        dut.core_top_0.M0_0.mem[idx].value = 0
        dut.core_top_0.M0_1.mem[idx].value = 0
    for idx in range (0, 512):
        dut.core_top_0.M1_0.mem[idx].value = random.randint(0, 2**256-1)
        dut.core_top_0.M1_1.mem[idx].value = random.randint(0, 2**256-1)
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")

    # program initialization
    imem_path = "../../software/pim_instr_test/pim_instr.hex"
    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    with open(imem_path, "r") as mem:
        first_line = mem.readline()
        idx  = 0
        for line in mem:
            inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
            inst_decimal = int(inst, 16)
            mux_addr = idx & 0x00000003     # 2-bit
            row_addr = (idx & 0x000003fc) >> 2     # 8-bit
            if idx < 1024:
                data =  dut.core_top_0.M0_0.mem[row_addr].value
                data = data | (((inst_decimal & 0x00000001) >> 0)  << ( 0*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000002) >> 1)  << ( 1*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000004) >> 2)  << ( 2*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000008) >> 3)  << ( 3*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000010) >> 4)  << ( 4*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000020) >> 5)  << ( 5*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000040) >> 6)  << ( 6*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000080) >> 7)  << ( 7*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000100) >> 8)  << ( 8*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000200) >> 9)  << ( 9*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000400) >> 10) << (10*4  + mux_addr))
                data = data | (((inst_decimal & 0x00000800) >> 11) << (11*4  + mux_addr))
                data = data | (((inst_decimal & 0x00001000) >> 12) << (12*4  + mux_addr))
                data = data | (((inst_decimal & 0x00002000) >> 13) << (13*4  + mux_addr))
                data = data | (((inst_decimal & 0x00004000) >> 14) << (14*4  + mux_addr))
                data = data | (((inst_decimal & 0x00008000) >> 15) << (15*4  + mux_addr))
                data = data | (((inst_decimal & 0x00010000) >> 16) << (16*4  + mux_addr))
                data = data | (((inst_decimal & 0x00020000) >> 17) << (17*4  + mux_addr))
                data = data | (((inst_decimal & 0x00040000) >> 18) << (18*4  + mux_addr))
                data = data | (((inst_decimal & 0x00080000) >> 19) << (19*4  + mux_addr))
                data = data | (((inst_decimal & 0x00100000) >> 20) << (20*4  + mux_addr))
                data = data | (((inst_decimal & 0x00200000) >> 21) << (21*4  + mux_addr))
                data = data | (((inst_decimal & 0x00400000) >> 22) << (22*4  + mux_addr))
                data = data | (((inst_decimal & 0x00800000) >> 23) << (23*4  + mux_addr))
                data = data | (((inst_decimal & 0x01000000) >> 24) << (24*4  + mux_addr))
                data = data | (((inst_decimal & 0x02000000) >> 25) << (25*4  + mux_addr))
                data = data | (((inst_decimal & 0x04000000) >> 26) << (26*4  + mux_addr))
                data = data | (((inst_decimal & 0x08000000) >> 27) << (27*4  + mux_addr))
                data = data | (((inst_decimal & 0x10000000) >> 28) << (28*4  + mux_addr))
                data = data | (((inst_decimal & 0x20000000) >> 29) << (29*4  + mux_addr))
                data = data | (((inst_decimal & 0x40000000) >> 30) << (30*4  + mux_addr))
                data = data | (((inst_decimal & 0x80000000) >> 31) << (31*4  + mux_addr))
                dut.core_top_0.M0_0.mem[row_addr].value = data
            else:
                ddata =  dut.core_top_0.M0_1.mem[row_addr].value
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
                dut.core_top_0.M0_1.mem[row_addr].value = ddata
            await RisingEdge(dut.i_clk)
            idx = idx + 1
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    dut.i_spi_rst_n.value = 1
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")


    # SPI flash program
    # dmem_path = "/home/pjy-wsl/rv32i/dmem.mem"
    #with open(imem_path, "r") as mem:
    #    first_line = mem.readline()
    #    idx  = 0x40000000
    #    for line in mem:
    #        inst = line.strip()  # Remove leading/trailing whitespaces and newline characters
    #        inst_decimal = int(inst, 16)
    #        #print("addr: \t", hex(idx)[2:].zfill(8))
    #        #print("data: \t", hex(inst_decimal)[2:].zfill(8))
    #        
    #        await cocotb.start_soon(write_sram(dut, spi_master, idx, inst_decimal))
    #        idx = idx + 4
    #        #if idx == 0x4000007c:
    #        #    break
    #        
    #await RisingEdge(dut.i_clk)
    #await Timer(1, units="ns")
    #await RisingEdge(dut.i_clk)
    #await Timer(1, units="ns")
    #print("Flash Program done")
    #
    ## SPI flash PIM buffer
    #idx  = 0x20000000
    #for i in range (0, 8192):
    #    if i % 100 == 0:
    #        print("Flash PIM buffer: ", i) 
    #    #print("addr: \t", hex(idx)[2:].zfill(8))
    #    #print("data: \t", hex(inst_decimal)[2:].zfill(8))
    #    await cocotb.start_soon(write_sram(dut, spi_master, idx, random.randint(0, 2**32-1)))
    #    idx = idx + 4
    #        #if idx == 0x4000007c:
    #        #    break


    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")
    dut.i_rv_rst_n.value = 1
    dut.i_spi_rst_n.value = 0
    await RisingEdge(dut.i_clk)
    await Timer(1, units="ns")

    for _ in range(10000):
        await RisingEdge(dut.i_clk)

    #assert dut.core_0.core_ID.rf.rf_data[3].value == 0xffffffff, "RVTEST_FAIL"






