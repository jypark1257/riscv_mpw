# Makefile for Icarus Verilog Simulation with SystemVerilog support

# Top-level testbench module
TOP_MODULE = mpw_sim

INCDIR = -I/home/jiyong/riscv_mpw/rtl/headers

# BIOS hex file
PIM_INSTR_SRC = ../../software/pim_instr/pim_instr.hex
PIM_INSTR_DST = ./pim_instr.hex

# Source files
SRC = ./tb_riscv.sv \
	  ./spi_master.sv \
      /home/jiyong/riscv_mpw/rtl/mpw_top.sv \
      /home/jiyong/riscv_mpw/rtl/core_top.sv \
      $(wildcard /home/jiyong/riscv_mpw/rtl/bus/*.sv) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/bus/*.v) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/core/*.sv) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/core/*.v) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/memory/*.sv) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/memory/*.v) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/peripheral/spi_slave/*.sv) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/peripheral/spi_slave/*.v) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/peripheral/uart/*.sv) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/peripheral/uart/*.v) \
      $(wildcard /home/jiyong/riscv_mpw/rtl/dma/pim_dma_v2.sv) 

# Output binary
OUT = sim.out

# Waveform file
WAVE = wave.vcd

# Default target: build and run
all: run

# Check and copy pim_instr
$(PIM_INSTR_DST):
	@if [ ! -f $(PIM_INSTR_SRC) ]; then \
		echo "[INFO] pim_instr.hex not found, attempting to build it..."; \
		make -C ../../software/pim_instr; \
	fi
	@if [ ! -f $(PIM_INSTR_SRC) ]; then \
		echo "[ERROR] Failed to generate pim_instr.hex. Aborting."; \
		exit 1; \
	fi
	cp $(PIM_INSTR_SRC) $(PIM_INSTR_DST)

# Compile
$(OUT): $(SRC) $(PIM_INSTR_DST)
	iverilog -g2012 $(INCDIR) -o $(OUT) -s $(TOP_MODULE) $(SRC)

# Run the simulation
run: $(OUT)
	vvp $(OUT)

# View waveform with GTKWave
wave: run
	gtkwave $(WAVE)

# Clean up generated files
clean:
	rm -f $(OUT) $(WAVE) $(PIM_INSTR_DST)
