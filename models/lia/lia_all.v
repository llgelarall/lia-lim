// Combined modules; select the desired module as synthesis/simulation top.
// Source: assets/codes/LIA/lia_00.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_Best
// Original rankadders.py label: 0; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_00 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        assign low_bits = ONES_BELOW_TOP | XOR_TOP;
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_01.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_MAE_PE_Best
// Original rankadders.py label: 1; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_01 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        assign low_bits = (OR_AB & ONES_BELOW_TOP) | XOR_TOP;
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_02.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_MSE_Best
// Original rankadders.py label: 2; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_02 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2 || LPL == 3) begin : g_lo_1
            assign low_bits = (OR_AB & ONES_BELOW_TOP) | XOR_TOP;
        end
        else begin : g_lo_2
            assign low_bits = ((((ONE << (LPL-3)) - ONE) | (OR_AB & (ONE << (LPL-3)))) | XOR_TOP);
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_03.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_MSE_Best_2
// Original rankadders.py label: 3; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_03 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2) begin : g_lo_1
            assign low_bits = (OR_AB & ONES_BELOW_TOP) | XOR_TOP;
        end
        else begin : g_lo_2
            assign low_bits = ((((ONE << (LPL-2)) - ONE) | (OR_AB & (ONE << (LPL-2)))) | XOR_TOP);
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_04.v
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


// Source: assets/codes/LIA/lia_05.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N25_LOA
// Original rankadders.py label: 5; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_05 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        assign low_bits = OR_AB & LOW_MASK;
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_06.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N25_2
// Original rankadders.py label: 6; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_06 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else begin : g_lo_1
            assign low_bits = (OR_AB & ONES_BELOW_TOP) | (NOT_BOTH << (LPL-1));
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_07.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N25_3
// Original rankadders.py label: 7; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_07 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = (LPL == 1) ? (TOP_A & TOP_B) : TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else begin : g_lo_1
            assign low_bits = (OR_AB & ONES_BELOW_TOP) | ((TOP_A & ~TOP_B) << (LPL-1));
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_08.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N25_4
// Original rankadders.py label: 8; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_08 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = (LPL == 1) ? (TOP_A & TOP_B) : TOP_A;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else begin : g_lo_1
            assign low_bits = (OR_AB & ONES_BELOW_TOP) | ((~TOP_A & TOP_B) << (LPL-1));
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_09.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_0_1
// Original rankadders.py label: 9; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_09 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = 1'b0;
        assign low_bits = LOW_MASK;
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_10.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_0_2
// Original rankadders.py label: 10; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_10 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2) begin : g_lo_1
            assign low_bits = (BEXT & ONE) | (NOT_BOTH << (LPL-1));
        end
        else begin : g_lo_2
            assign low_bits = (OR_AB & ONES_BELOW_TOP & ~ONE) | (BEXT & ONE) | (NOT_BOTH << (LPL-1));
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_11.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_P25
// Original rankadders.py label: 11; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_11 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2) begin : g_lo_1
            assign low_bits = (OR_AB & ONE) | XOR_TOP;
        end
        else begin : g_lo_2
            assign low_bits = ((ONE << (LPL-1)) - (ONE << 1)) | (OR_AB & ONE) | XOR_TOP;
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_12.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_N50_1
// Original rankadders.py label: 12; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_12 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2) begin : g_lo_1
            assign low_bits = ONE | (NOT_BOTH << (LPL-1));
        end
        else begin : g_lo_2
            assign low_bits = (OR_AB & ONES_BELOW_TOP & ~ONE) | ONE | (NOT_BOTH << (LPL-1));
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule


// Source: assets/codes/LIA/lia_13.v
// Auto-translated from LFAs.c: unsgn_LFA_21_21_ME_P50
// Original rankadders.py label: 13; valid for 0 <= LPL < N (and extended to LPL == N).
// Output is N+1 bits (carry-out is retained).
module lia_13 #(parameter integer N=12, parameter integer LPL=6) (
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
        wire carry_to_upper = TOP_A & TOP_B;
        if (LPL == 1) begin : g_lo_0
            assign low_bits = XOR_TOP;
        end
        else if (LPL == 2) begin : g_lo_1
            assign low_bits = (BEXT & ONE) | XOR_TOP;
        end
        else if (LPL == 3) begin : g_lo_2
            assign low_bits = (OR_AB & (ONE << 1)) | ONE | XOR_TOP;
        end
        else begin : g_lo_3
            assign low_bits = (((ONE << (LPL-3)) - ONE) << 2) | (OR_AB & (ONE << 1)) | ONE | XOR_TOP;
        end
        wire [N:0] upper_sum = (AEXT >> LPL) + (BEXT >> LPL) + carry_to_upper;
        assign y = (upper_sum << LPL) | low_bits;
      end
    endgenerate
endmodule
