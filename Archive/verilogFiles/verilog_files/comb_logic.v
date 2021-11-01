module  comb_logic(input A, B, C, output Out);
// Random comb logic
always @ (A,B,C)
begin
	case({A,B,C})
	3'b000: {Out} = 1'b1;
	3'b001: {Out} = 1'b0;
	3'b010: {Out} = 1'b1;
	3'b011: {Out} = 1'b0;
	3'b100: {Out} = 1'b0;
	3'b101: {Out} = 1'b0;
	3'b110: {Out} = 1'b0;
	3'b111: {Out} = 1'b1;
	endcase
end
endmodule