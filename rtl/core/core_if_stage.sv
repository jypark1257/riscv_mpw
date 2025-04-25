
module core_if_stage #(
    parameter XLEN      = 32,
    parameter RESET_PC  = 32'h1000_0000
) (
    input                       clk_i,
    input                       rst_ni,
    input                       pc_write_i,
    input                       branch_taken_i,
    input   [XLEN-1:0]          pc_branch_i,
    output  logic   [XLEN-1:0]  pc_curr_o,
    output  logic   [XLEN-1:0]  pc_instr_o
);

    // Program counter
    logic [XLEN-1:0] pc_next;
    logic [XLEN-1:0] pc_plus_2;
    //logic [XLEN-1:0] pc_plus_4;
    logic [XLEN-1:0] pc_branch_plus_2;
    //logic [XLEN-1:0] pc_branch_plus_4;

    assign pc_plus_2 = pc_curr_o + 2;
    //assign pc_plus_4 = pc_curr_o + 4;
    assign pc_branch_plus_2 = pc_branch_i + 2;
    //assign pc_branch_plus_4 = pc_branch_i + 4;

    always_comb begin
        pc_next  = RESET_PC;
        if (branch_taken_i) begin
            pc_next = pc_branch_plus_2;
        end else begin
            pc_next = pc_plus_2;
        end
    end

    // assign pc_next = (branch_taken_i) ? pc_branch_plus_4 : pc_plus_4;

    program_counter #(
        .XLEN       (XLEN),
        .RESET_PC   (RESET_PC)
    ) pc (
        .clk_i      (clk_i),
        .rst_ni     (rst_ni),
        .pc_write_i (pc_write_i),
        .pc_next_i  (pc_next),
        .pc_curr_o  (pc_curr_o)
    );

    // --------------------------------------------------------

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (rst_ni == 1'b0) begin
            pc_instr_o <= '0;
        end else begin
            if (branch_taken_i) begin
                pc_instr_o <= pc_branch_i;
            end else begin
                pc_instr_o <= pc_curr_o;
            end
        end
    end

endmodule