// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N50_2
// Original rankadders.py label: 4; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_04 #(parameter integer N=12, parameter integer LPL=6) (
    input wire [N-1:0] a,
    input wire [N-1:0] b,
    output wire [N:0] y
);
    generate
      if (LPL == 0) begin : g_precise
        assign y = {1'b0,a} + {1'b0,b};
      end else begin : g_approx
        localparam [N:0] ONE = {{N{1'b0}},1'b1};
        localparam [N:0] LOW_MASK = ({(N+1){1'b1}} >> (N+1-LPL));
        wire [N:0] AEXT = {1'b0,a};
        wire [N:0] BEXT = {1'b0,b};
        wire [N:0] OR_AB = AEXT | BEXT;
        wire [N:0] ONES_BELOW_TOP = LOW_MASK >> 1;
        wire TOP_A = a[LPL-1];
        wire TOP_B = b[LPL-1];
        wire [N:0] XOR_TOP = ({{N{1'b0}},(TOP_A ^ TOP_B)} << (LPL-1));
        wire [N:0] NOT_BOTH = {{N{1'b0}},(~(TOP_A & TOP_B))};
        wire [N:0] low_bits;
        wire carry_to_upper = TOP_B;
        assign low_bits = AEXT & LOW_MASK;
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule
