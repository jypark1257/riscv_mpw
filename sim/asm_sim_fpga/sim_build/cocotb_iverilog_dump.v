module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/core_top.fst");
    $dumpvars(0, core_top);
end
endmodule
