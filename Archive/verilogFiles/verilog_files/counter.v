//2 bit counter. Counts from 1-4, or 0-3
module up_counter(input clk, output[1:0] counter);
reg [1:0] counter_up;

always @(posedge clk)
begin
    case(counter_up)
        2'b00:    
        begin
            {counter} = 2'b01;
            {counter_up} = 2'b01;
        end
        2'b01:    
        begin
            {counter} = 2'b10;
            {counter_up} = 2'b10;
        end
        2'b10:    
        begin
            {counter} = 2'b11;
            {counter_up} = 2'b11;
        end
        2'b11:    
        begin
            {counter} = 2'b00;
            {counter_up} = 2'b00;
        end
        default:
        begin
            {counter} = 2'b00;
            {counter_up} = 2'b00;
        end

    endcase
end
endmodule