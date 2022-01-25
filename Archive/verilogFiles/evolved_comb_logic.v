module  evolved_comb_logic(
    A      , 
    B      , 
    C     , 
    D ,
    Out      
);
input A, B, C, D ;
output Out;
wire nand_0, xor_0, xor_1, not_0, nor_0, xor_2, and_0, or_0, nor_1, nor_2, or_1;

nand NAND0 (nand_0, C, A);
xor XOR0 (xor_0, B, A);
xor XOR1 (xor_1, xor_0, nand_0);
not NOT0 (not_0, A);
nor NOR0 (nor_0, not_0, xor_1);
xor XOR2 (xor_2, nor_0, A);
and AND0 (and_0, A, A);
or OR0 (or_0, and_0, D);
nor NOR1 (nor_1, or_0, D);
nor NOR2 (nor_2, nor_1, xor_2);
or OR1 (or_1, nor_2, C);
xor XOR3(Out, C, or_1);)

endmodule