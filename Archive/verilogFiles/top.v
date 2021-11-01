// Bayley King, Bryan Kanu, Zach Hadden
// Embedded Systems final project
// Top level wrapper for project

`timescale 1ns / 100ps

module top(clk, rst, enable, switches, sign, ready, underflow, overflow,
           inexact, exception, invalid, UART_TXD
);

input       I0;
input       I1;
input       sel;

// led outputs
output      out;

wire mux_out_ev;
wire mux_out_ast;

debouncer u1 (
    .pb_1(enable), .clk(clk), .pb_out(enable_deb)
);

evolved_mux_using_ast U0(
    .I0(I0), 
    .I1(I1), 
    .sel(sel), 
    .mux_out(mux_out_ev)
);

mux_using_ast U1(
    .I0(I0), 
    .I1(I1), 
    .sel(sel), 
    .mux_out(mux_out_ast)
);



always @ (posedge clk) begin
    
    
end

assign out = mux_out_ev xnor mux_out_ast;

endmodule
