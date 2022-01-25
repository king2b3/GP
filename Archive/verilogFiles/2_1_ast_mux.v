module  mux_using_ast(
    I0      , 
    I1      , 
    sel     , 
    mux_out      
);
input I0, I1, sel ;
output mux_out;
wire  nand_0, nand_1, nand_2 ;

nand NAND_0 (nand_0, I0, sel);
nand NAND_1 (nand_1, sel, sel);
nand NAND_2 (nand_2, nand_1, I1);
nand NAND_3 (mux_out, nand_0, nand_2);

endmodule 
