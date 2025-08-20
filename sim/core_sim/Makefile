# Makefile for Icarus Verilog Simulation with SystemVerilog support

# Top-level testbench module
TOP_MODULE = mpw_sim

INCDIR = -I../../rtl/headers

# BIOS hex file
BIOS_SRC = ../../software/bios/bios.hex
BIOS_DST = ./bios.hex

DEFINES = -DDW_SUPPRESS_WARN -DMY_PARAM=16

# Source files
SRC = ./tb_riscv.sv \
	  ./spi_master.sv \
      ../../rtl/mpw_top.sv \
      ../../rtl/core_top.sv \
      $(wildcard ../../rtl/bus/*.sv) \
      $(wildcard ../../rtl/bus/*.v) \
      $(wildcard ../../rtl/core/*.sv) \
      $(wildcard ../../rtl/core/*.v) \
      $(wildcard ../../rtl/memory/*.sv) \
      $(wildcard ../../rtl/memory/*.v) \
      $(wildcard ../../rtl/peripheral/spi_slave/*.sv) \
      $(wildcard ../../rtl/peripheral/spi_slave/*.v) \
      $(wildcard ../../rtl/peripheral/peri_module/peri_module/*.sv) \
      $(wildcard ../../rtl/peripheral/peri_module/peri_module/output_buffer/*.sv) \
      $(wildcard ../../rtl/peripheral/spi_slave/*.v) \
      $(wildcard ../../rtl/peripheral/uart/*.sv) \
      $(wildcard ../../rtl/peripheral/uart/*.v) \
      $(wildcard ../../rtl/dma/pim_dma_v2.sv) 

# Output binary
OUT = sim.out

# Waveform file
WAVE = wave.vcd

# Default target: build and run
all: run

# Check and copy BIOS
$(BIOS_DST):
	@if [ ! -f $(BIOS_SRC) ]; then \
		echo "[INFO] bios.hex not found, attempting to build it..."; \
		make -C ../../software/bios; \
	fi
	@if [ ! -f $(BIOS_SRC) ]; then \
		echo "[ERROR] Failed to generate bios.hex. Aborting."; \
		exit 1; \
	fi
	cp $(BIOS_SRC) $(BIOS_DST)

# Compile
$(OUT): $(SRC) $(BIOS_DST)
	iverilog -g2012 $(INCDIR) $(DEFINES) -o $(OUT) -s $(TOP_MODULE) $(SRC)

# Run the simulation
run: $(OUT)
	vvp $(OUT)

# View waveform with GTKWave
wave: run
	gtkwave $(WAVE)

# Clean up generated files
clean:
	rm -f $(OUT) $(WAVE) $(BIOS_DST)
