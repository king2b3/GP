module  evolved_mux_using_ast(
    I0      , 
    I1      , 
    sel     , 
    mux_out      
);
input I0, I1, sel ;
output mux_out;
wire  and_0, and_1, nand_0, nand_1, nand_2, or_0, or_1, or_2;

and AND_0 (and_0, I1, sel);
and AND_1 (and_1, I1, and_0);
or OR_0 (or_0, I0, I1);
or OR_1 (or_1, I1, sel);
or OR_2 (or_2, I1, or_1);
nand NAND_0 (nand_0, and_1, or_0);
nand NAND_1 (nand_1, nand_0, I1);
nand NAND_2 (nand_2, I0, or_2);
nand NAND_3 (mux_out, nand_1, nand_2);

endmodule 
