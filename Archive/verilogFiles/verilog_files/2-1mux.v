module  mux_using_assign(in0, in1, sel, mux_out);
// 2-1 MUX (multiplexer)
always @(in0,in1,sel) begin
	case(sel)
	1'b0: 	mux_out = in0;
	1'b1:	mux_out = in1;
	endcase
end
endmodule 