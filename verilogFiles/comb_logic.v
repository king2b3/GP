module  comb_logic(A, B, C, D, Out);
// gate level verilog
// Random comb logic

input A, B, C, D ;
output Out;
wire and_0, and_1, and_2, xor_0, and_3, or_0, nor_0, nor_1;

and AND0 (and_0, C, B);
and AND1 (and_1, and_0, C);
and AND2 (and_2, and_1, C);
xor XOR0 (xor_0, and_2, B);
and AND3 (and_3, xor_0, A);
or OR0 (or_0, and_3, C);
nor NOR0 (nor_0, D, A);
nor NOR1 (Out, nor_0, or_0);

endmodule
