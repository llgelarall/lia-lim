// Parameterized from uploaded lim_me_p50.v / original LFMs.c.
// N: operand bits; LPL: number of approximate least-significant PRODUCT bits.
// 0 <= LPL <= N; N <= 12 supported by original C reference test harness.
module lim_me_p50 #(parameter integer N=8, parameter integer LPL=8)
 (input wire [N-1:0] A, input wire [N-1:0] B, output wire [2*N-1:0] O);
localparam integer W = 2*N;
generate if (N < 2 || LPL < 0 || LPL > N) begin : invalid_parameters
  INVALID_N_OR_LPL_CONFIGURATION invalid();
end else if (LPL == 0) begin : precise
  assign O = A * B;
end else begin : approximate
  wire [W-1:0] pp [0:N-1];
  genvar i;
  for (i=0; i<N; i=i+1) begin : partial_products
    assign pp[i] = B[i] ? ({{N{1'b0}},A} << i) : {W{1'b0}};
  end
  reg [W-1:0] high_sum;
  integer j;
  always @* begin
    high_sum = {W{1'b0}};
    for (j=0;j<N;j=j+1)
      high_sum = high_sum + (pp[j] >> LPL);
    high_sum = high_sum + ((A[LPL-1] & B[LPL-1]) ? ((LPL > 3) ? (LPL-3) : 0) : 0);
  end
  wire [LPL-1:0] low;
  genvar g;
  for(g=0;g<LPL;g=g+1) begin : low_bits
    if (LPL >= 4) begin : general
      if (g == 0) begin assign low[g] = (A[0] & B[0]); end
      else if (g == 1) begin assign low[g] = (A[1] & B[1]); end
      else if (g == LPL-1) begin assign low[g] = (~A[LPL-1] & ~B[LPL-1]) | (~A[LPL-1] & B[LPL-1]) | (A[LPL-1] & ~B[LPL-1]); end
      else if (g == 2) begin assign low[g] = (A[g] & B[g]); end
      else begin assign low[g] = (A[g] & B[g]); end
    end else begin : g_small
      // Boolean lookup indexed by the two input bits, 00, 01, 10, 11.
      wire [1:0] idx = {A[g],B[g]};
      if (LPL == 1) begin
        assign low[g] = ((4'b0000 >> idx) & 1'b1);
      end else if (LPL == 2) begin
        if(g==0) assign low[g] = ((4'b1000 >> idx) & 1'b1);
        else assign low[g] = ((4'b1000 >> idx) & 1'b1);
      end else begin
        if(g==0) assign low[g] = ((4'b1000 >> idx) & 1'b1);
        else if(g==1) assign low[g] = ((4'b1000 >> idx) & 1'b1);
        else assign low[g] = ((4'b1110 >> idx) & 1'b1);
      end
    end
  end
  assign O = (high_sum << LPL) | {{(W-LPL){1'b0}},low};
end endgenerate
endmodule
