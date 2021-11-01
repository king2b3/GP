module  mux_using_assign(input a, b, c, d, output e);
// 2-1 MUX (multiplexer)
always @(a,b,c,d) begin
	case(a,b,c,d)
	4'b0000: 	e = 0;
	4'b0001:	e = 0;
	4'b0010: 	e = 0;
	4'b0011:	e = 0;
	4'b0100: 	e = 0;
	4'b0101:	e = 0;
	4'b0110: 	e = 0;
	4'b0111:	e = 0;
	4'b0100: 	e = 0;
	4'b1001:	e = 0;
	4'b1010: 	e = 0;
	4'b1011:	e = 0;
	4'b1100: 	e = 0;
	4'b1101:	e = 0;
	4'b1110: 	e = 1;
	4'b1111:	e = 1;
	endcase
end
endmodule 