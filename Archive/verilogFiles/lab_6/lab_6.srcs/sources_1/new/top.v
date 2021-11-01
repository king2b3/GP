`timescale 1ns / 1ps


module multiplier(product, x, y);
output reg [5:0] product;
input [1:0] x;
input [3:0] y;
    always @(x, y)
        product = x * y;
endmodule

/////////////////////////////////////////////

module adder(sum, a, b);
input [5:0] a, b;
output reg [5:0] sum;
    always @(a, b)
        sum = a + b;
endmodule

/////////////////////////////////////////////

module Top(A1, B1, B2, m);
input [3:0] A1;
input [1:0] B1, B2;
output [7:0] m;
wire [5:0] product1, product2;
wire [5:0] bus1;
wire [5:0] n;

    assign bus1 = product1[5:2];
    multiplier multiplier1 (product1, B1, A1);
    multiplier multiplier2 (product2, B2, A1);
    adder adder1 (n, product2, bus1);
    assign m = {n, product1[1:0]};
endmodule 

