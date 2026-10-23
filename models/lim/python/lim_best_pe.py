"""lim_best_pe: extracted without arithmetic changes from assets/codes/LIMs.ipynb.
Validated domain: unsigned N=8, LPL=1..7.
Call compute(a,b,8,8,lpl).
"""
import sys

class LIMComponents:
    def unsgn_LFM_Best_PE(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Best PE Approximation.
        """
        number2 = op2
        sum_val = 0
        imprecise_part = 0

        pp = [0] * wl2
        # Ensure S array is large enough to handle up to VBL iterations
        s = [0] * max(wl2, vbl) 

        # Extract bits of op2 to form partial products
        for i in range(wl2):
            pp[i] = (number2 % 2) * op1
            number2 = number2 // 2

        # Shift partial products by their weight
        for i in range(wl2):
            pp[i] = pp[i] * (2 ** i)

        # Truncate partial products by VBL
        for i in range(wl2):
            pp[i] = pp[i] >> vbl

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        # Imprecise part construction logic for PE
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) | (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) ^ (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = (part_1 & part_2) >> i
                elif i == 1:
                    s[i] = (part_1 ^ part_2) >> i
                else:
                    s[i] = (part_1 | part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)


unsgn_LFM_Best_PE = LIMComponents.unsgn_LFM_Best_PE
compute = unsgn_LFM_Best_PE
