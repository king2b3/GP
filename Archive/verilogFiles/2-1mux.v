module  mux_using_assign(in0, in1, sel, mux_out);

// 2-1 MUX (multiplexer)

input in0, in1, sel ;
output mux_out;
wire  mux_out;
// ? is a way to do a one line if statement. if sel is ON then in1, else in0.
assign mux_out = (sel) ? in1 : in0;

endmodule 
