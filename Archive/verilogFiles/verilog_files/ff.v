module RisingEdge_DFlipFlop(input D,clk, output Q);
// This is really bad, but not often to do a FF like this. 

always @(clk) 
begin
	case(D)
	1'b0:	{Q} = 1'b0;
	1'b1:	{Q} = 1'b1;
	endcase
end
endmodule