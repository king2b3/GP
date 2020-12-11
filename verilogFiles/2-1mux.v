module  mux_using_assign(
in0      , 
in1      , 
sel        , 
mux_out      
);
input in0, in1, sel ;
output mux_out;
wire  mux_out;
assign mux_out = (sel) ? in1 : in0;

endmodule 
