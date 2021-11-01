module  main(X, Y, Z, O);
input X, Y, Z ;
output O;
wire  O;
assign O =~ (X & Y) | (Y & Z) | (X & Z);

endmodule 
