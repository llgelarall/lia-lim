"""lim_equal_arch_me_p25: extracted without arithmetic changes from assets/codes/LIMs.ipynb.
Validated domain: unsigned N=8, LPL=1..7.
Call compute(a,b,8,8,lpl).
"""
import sys

class LIMComponents:
    def unsgn_LFM_Equal_Arch_ME_P25(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Equal Architecture ME P25 Approximation.
        Note: The imprecise part generation is explicitly omitted in this architecture.
        """
        number2 = op2
        sum_val = 0

        pp = [0] * wl2

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

        # Carry injection logic for P25 (Uses VBL - 1)
        if vbl > 1:
            c_0_x = ((op1 & (1 << (vbl - 1))) & (op2 & (1 << (vbl - 1)))) >> (vbl - 1)
            sum_val = (vbl - 1) * c_0_x

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        return int(sum_val)


unsgn_LFM_Equal_Arch_ME_P25 = LIMComponents.unsgn_LFM_Equal_Arch_ME_P25
compute = unsgn_LFM_Equal_Arch_ME_P25
