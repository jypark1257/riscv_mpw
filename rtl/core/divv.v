module divv #(
  	parameter a_width  = 32,
  	parameter b_width  = 32
) (
	input  			[a_width-1 : 0] a,
  	input  			[b_width-1 : 0] b,
  	output reg		[a_width-1 : 0] quotient,
  	output reg		[b_width-1 : 0] remainder
);

	wire [a_width-1 : 0] quotient_tmp;
	wire [b_width-1 : 0] remainder_tmp;

    DW_div #(
        .a_width        (a_width),
        .b_width        (b_width),
        .tc_mode        (1'b1),
        .rem_mode       (1'b1)
	) DW_div_signed (
        .a              (a), 
        .b              (b), 
        .quotient       (quotient_tmp), 
        .remainder      (remainder_tmp), 
        .divide_by_0    ()
    );

	always @(*) begin
		quotient = quotient_tmp;
		remainder = remainder_tmp;

		if ((a == 32'h80000000) && (b == {32{1'b1}})) begin		//signed overflow
			quotient = a;
			remainder = 32'b0;
		end else if (b == 0) begin		//devide by zero
			quotient = {a_width{1'b1}};
		end
	end

endmodule