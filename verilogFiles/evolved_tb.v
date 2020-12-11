`timescale 1ns / 1ps

module ast_tb;
reg I0;
reg I1;
reg sel;
reg clk;
wire mux_out_ast;
wire mux_out_ev;
   
    evolved_mux_using_ast UUT(
        .I0(I0), 
        .I1(I1), 
        .sel(sel), 
        .mux_out(mux_out_ev)
    );

    mux_using_ast UUUT(
        .I0(I0), 
        .I1(I1), 
        .sel(sel), 
        .mux_out(mux_out_ast)
    );

always
    begin
        clk = 1'b1;
        #10;

        clk = 1'b0;
        #10;
    end    

always @(posedge clk)
    begin
        // 000
        I0=0; I1=0; sel=0; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end
        // 001
        I0=0; I1=0; sel=1; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end
        // 010
        I0=0; I1=1; sel=0; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end
        // 011
        I0=0; I1=1; sel=1; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end
        // 100
        I0=1; I1=0; sel=0; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end 
        // 101
        I0=1; I1=0; sel=1; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end    
        // 110
        I0=1; I1=1; sel=0; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end     
        // 111
        I0=1; I1=1; sel=1; #10;
        if (mux_out_ast == mux_out_ev) begin
            $display($time," ",I0,I1,sel," ","pass"); #10;
        end else begin
            $display($time," ",I0,I1,sel," ","fail"); #10;
        end
        $stop;
    end

endmodule
