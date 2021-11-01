module full_adder(output S, Cout, input A, B, Cin);
   always @(A, B, Cin)
   begin
      case({A,B,Cin})
      3'b000: 
       begin
          {Cout} = 1'b0;
          {S} = 1'b0;
       end
      3'b001: 
       begin
          {Cout} = 1'b0;
          {S} = 1'b1;
       end
       3'b010: 
       begin
          {Cout} = 1'b0;
          {S} = 1'b1;
       end
       3'b011: 
       begin
          {Cout} = 1'b1;
          {S} = 1'b0;
       end
       3'b100: 
       begin
          {Cout} = 1'b0;
          {S} = 1'b1;
       end
       3'b101: 
       begin
          {Cout} = 1'b1;
          {S} = 1'b0;
       end
       3'b110: 
       begin
          {Cout} = 1'b1;
          {S} = 1'b0;
       end
       3'b111: 
       begin
          {Cout} = 1'b1;
          {S} = 1'b1;
       end
   end
endmodule // full_adder