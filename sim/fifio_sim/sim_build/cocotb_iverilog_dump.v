module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/fifo_unit.fst");
    $dumpvars(0, fifo_unit);
end
endmodule
