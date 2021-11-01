`timescale 1ns / 1ps

module test;
    
    // Inputs  always reg
	reg [3:0] A1;
	reg [1:0] B1, B2;
	// Outputs  always wire
	wire [7:0] m;
	
	
	// Instantiate the Unit Under Test (UUT)
	Top uut (A1, B1, B2, m);                 // circuit 1
    
	initial begin
		// Initialize Inputs
		
		A1 = 'b0; B1 = 0; B2 = 0; #100;         // all zero
		A1 = 'ha; B1 = 3; B2 = 3; #100;        // max values (all ones)
		A1 = 15; B1 = 0; B2 = 0; #100;
		A1 = 4'b0000; B2 = 3; B2 = 3; #100;
		
        A1 = 1; B1 = 1; B2 = 1; #100;         // normal tests
        A1 = 10; B1 = 2; B2 = 3; #100;
		A1 = 6; B1 = 3; B2 = 0; #100;
		A1 = 15; B1 = 3; B2 = 2;

	 end  
   
endmodule

