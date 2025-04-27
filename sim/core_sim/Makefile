# Makefile for Icarus Verilog Simulation with SystemVerilog support

# Top-level testbench module
TOP_MODULE = mpw_sim

INCDIR = -I/home/pjy-wsl/riscv_mpw_v2/rtl/headers


# Source files
SRC = ./tb_riscv.sv \
	  ./spi_master.sv \
      /home/pjy-wsl/riscv_mpw_v2/rtl/mpw_top.sv \
      /home/pjy-wsl/riscv_mpw_v2/rtl/core_top.sv \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/bus/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/bus/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/core/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/core/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/memory/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/memory/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/peripheral/spi_slave/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/peripheral/spi_slave/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/peripheral/uart/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/peripheral/uart/*.v) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/dma/*.sv) \
      $(wildcard /home/pjy-wsl/riscv_mpw_v2/rtl/dma/*.v)

# Output binary
OUT = sim.out

# Waveform file
WAVE = wave.vcd

# Default target: build and run
all: run

# Compile
$(OUT): $(SRC)
	iverilog -g2012 $(INCDIR) -o $(OUT) -s $(TOP_MODULE) $(SRC)

# Run the simulation
run: $(OUT)
	vvp $(OUT)

# View waveform with GTKWave
wave: run
	gtkwave $(WAVE)

# Clean up generated files
clean:
	rm -f $(OUT) $(WAVE)
