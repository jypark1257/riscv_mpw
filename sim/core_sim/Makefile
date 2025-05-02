# Makefile for Icarus Verilog Simulation with SystemVerilog support

# Top-level testbench module
TOP_MODULE = mpw_sim

INCDIR = -I/home/pjy-wsl/riscv_mpw/rtl/headers

# BIOS hex file
BIOS_SRC = ../../software/bios/bios.hex
BIOS_DST = ./bios.hex

# Source files
SRC = ./tb_riscv.sv \
	  ./spi_master.sv \
      /home/pjy-wsl/riscv_mpw/rtl/mpw_top.sv \
      /home/pjy-wsl/riscv_mpw/rtl/core_top.sv \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/bus/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/bus/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/core/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/core/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/memory/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/memory/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/peripheral/spi_slave/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/peripheral/spi_slave/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/peripheral/uart/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/peripheral/uart/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/dma/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw/rtl/dma/*.v)

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
	iverilog -g2012 $(INCDIR) -o $(OUT) -s $(TOP_MODULE) $(SRC)

# Run the simulation
run: $(OUT)
	vvp $(OUT)

# View waveform with GTKWave
wave: run
	gtkwave $(WAVE)

# Clean up generated files
clean:
	rm -f $(OUT) $(WAVE) $(BIOS_DST)
