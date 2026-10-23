"""lim_me_p50: extracted without arithmetic changes from assets/codes/LIMs.ipynb.
Validated domain: unsigned N=8, LPL=1..7.
Call compute(a,b,8,8,lpl).
"""
import sys

class LIMComponents:
    def unsgn_LFM_ME_P50(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME P50 Approximation.
        """
        number2 = op2
        sum_val = 0
        imprecise_part = 0

        pp = [0] * wl2
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

        # Carry injection block
        if vbl - 3 > 0:
            c_0_x = ((op1 & (1 << (vbl - 1))) & (op2 & (1 << (vbl - 1)))) >> (vbl - 1)
            sum_val = (vbl - 3) * c_0_x

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        # Imprecise part construction logic for ME_P50
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = (part_1 & part_2) >> i
                elif i == (vbl - 1):
                    # Simulating the C 1-bit unsigned bitfield bitwise NOT behavior
                    s[i] = (~((part_1 & part_2) >> i)) & 1
                else:
                    s[i] = (part_1 & part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)


unsgn_LFM_ME_P50 = LIMComponents.unsgn_LFM_ME_P50
compute = unsgn_LFM_ME_P50
