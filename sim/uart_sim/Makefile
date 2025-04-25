# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
# CORE HEADERS
VERILOG_SOURCES += $(shell pwd)/../../rtl/headers/pipe_reg.svh
VERILOG_SOURCES += $(shell pwd)/../../rtl/headers/opcode.svh

# CORE TOP
VERILOG_SOURCES += $(shell pwd)/../../rtl/core_top.sv

# CORE
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/core.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/core_if_stage.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/core_id_stage.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/core_ex_stage.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/core_wb_stage.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/program_counter.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/compressed_decoder.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/decoder.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/immediate_generator.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/register_file.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/branch_unit.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/forwarding_unit.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/alu_control_unit.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/alu.sv

#VERILOG_SOURCES += $(shell pwd)/../../rtl/core/divv.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/DW_div.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/DW_div_pipe.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/DW02_mult_3_stage.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/DW02_mult_2_stage.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/core/muldiv_unit.sv

# DMA
VERILOG_SOURCES += $(shell pwd)/../../rtl/dma/pim_dma.sv

# SPI SLAVE
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/spi_slave/spi_slave_wrap.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/spi_slave/spi_slave.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/spi_slave/rising_edge_detect.sv

# UART 
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/uart/uart_wrap.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/uart/uart_wrap_test.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/uart/uart.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/uart/uart_transmitter.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/uart/uart_receiver.v

# PIM WRAPPER 
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/activation_buffer.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/pim.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/pim_controller_1.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/result_buffer.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/weight_buffer.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/PIM_1_TOP.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/peripheral/pim_wrap/WL_driver.v


# BUS
VERILOG_SOURCES += $(shell pwd)/../../rtl/bus/sys_bus.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/bus/bus_arbiter.sv

# MEMORY
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/imem.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/dmem.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/pim_buffer.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/ram_block_imem.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/ram_block_dmem.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/ram_block_buf.sv
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/sram_1024w_8b.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/sram_1024w_32b.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/sram_4096w_8b.v
VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/sram_4096w_32b.v
# VERILOG_SOURCES += $(shell pwd)/../../rtl/memory/sram_8192w_32b.v


COMPILE_ARGS += -DCOCOTB
TOPLEVEL = core_top
MODULE = test_asm

include $(shell cocotb-config --makefiles)/Makefile.sim