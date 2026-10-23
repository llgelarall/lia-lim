"""All LIM software models. Original notebook arithmetic retained.
Use COMPONENTS[architecture_id](...) or the original class methods.
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


    def unsgn_LFM_Best_MAE(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Best MAE Approximation.
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

        # Imprecise part construction logic for MAE
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
                elif i == 1:
                    s[i] = (part_1 | part_2) >> i
                else:
                    s[i] = (part_1 | part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)



    def unsgn_LFM_ME_0(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME 0 Approximation.
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

        # Imprecise part construction logic for ME_0
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) | (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) | (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = (part_1 | part_2) >> i
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


    def unsgn_LFM_ME_P25(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME P25 Approximation.
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

        # Imprecise part construction logic for ME_P25
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = part_1 >> i
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


    def unsgn_LFM_ME_P75(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME P75 Approximation.
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

        # Imprecise part construction logic for ME_P75
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = 0
        elif vbl == 3:
            s[0] = 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = 0
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


    def unsgn_LFM_ME_N25(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME N25 Approximation.
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

        # Imprecise part construction logic for ME_N25
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = (op1 & (1 << 1)) >> 1
        elif vbl == 3:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = (op1 & (1 << 1)) >> 1
            s[2] = ((op1 & (1 << 2)) | (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0 or i == 1:
                    s[i] = part_1 >> i
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


    def unsgn_LFM_ME_N50(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME N50 Approximation.
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

        # Imprecise part construction logic for ME_N50
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) | (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = 1
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                # Cleaned up conditional hierarchy compared to C
                if i == 0 or i == 1:
                    s[i] = (part_1 & part_2) >> i
                elif i == 2:
                    s[i] = part_1 >> i
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


    def unsgn_LFM_ME_N75(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM ME N75 Approximation.
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

        # Imprecise part construction logic for ME_N75
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = ((op1 & (1 << 1)) | (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = 1
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                if i == 0:
                    s[i] = part_1 >> i
                elif i == 1:
                    s[i] = (part_1 & part_2) >> i
                elif i == 2:
                    s[i] = part_1 >> i
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


    def unsgn_LFM_Equal_Arch_PE(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Equal Architecture PE Approximation.
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

        # Carry injection logic is commented out in original C code
        # if vbl - 3 > 0:
        #     c_0_x = ((op1 & (1 << (vbl - 1))) & (op2 & (1 << (vbl - 1)))) >> (vbl - 1)
        #     sum_val = (vbl - 3) * c_0_x

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        # Imprecise part construction logic
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) & (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                s[i] = (part_1 & part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)


    def unsgn_LFM_Equal_Arch_MSE(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Equal Architecture MSE Approximation.
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

        # Carry injection logic is commented out in original C code
        # if vbl - 3 > 0:
        #     c_0_x = ((op1 & (1 << (vbl - 1))) & (op2 & (1 << (vbl - 1)))) >> (vbl - 1)
        #     sum_val = (vbl - 3) * c_0_x

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        # Imprecise part construction logic
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = (op1 & (1 << 0)) >> 0
            s[1] = (op1 & (1 << 1)) >> 1
            s[2] = (op1 & (1 << 2)) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                s[i] = (part_1 | part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)


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


    def unsgn_LFM_Equal_Arch_ME_P50(op1: int, op2: int, wl1: int, wl2: int, vbl: int) -> int:
        """
        Main Logic Function for LFM Equal Architecture ME P50 Approximation.
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

        # Carry injection logic for P50 (Uses VBL - 2)
        if vbl - 2 > 0:
            c_0_x = ((op1 & (1 << (vbl - 1))) & (op2 & (1 << (vbl - 1)))) >> (vbl - 1)
            sum_val = (vbl - 2) * c_0_x

        # Sum the truncated partial products
        for i in range(wl2):
            sum_val += pp[i]

        # Shift the sum back to its correct weight
        sum_val = sum_val * (2 ** vbl)

        # Imprecise part construction logic
        if vbl == 1:
            s[0] = 0
        elif vbl == 2:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
        elif vbl == 3:
            s[0] = ((op1 & (1 << 0)) & (op2 & (1 << 0))) >> 0
            s[1] = ((op1 & (1 << 1)) & (op2 & (1 << 1))) >> 1
            s[2] = ((op1 & (1 << 2)) & (op2 & (1 << 2))) >> 2
        elif vbl > 3:
            for i in range(vbl):
                part_1 = op1 & (1 << i)
                part_2 = op2 & (1 << i)
                s[i] = (part_1 & part_2) >> i

        # Reconstruct the imprecise part integer
        for i in range(vbl):
            imprecise_part += s[i] * (2 ** i)

        sum_val += imprecise_part

        return int(sum_val)



unsgn_LFM_Best_MAE = LIMComponents.unsgn_LFM_Best_MAE
unsgn_LFM_Best_PE = LIMComponents.unsgn_LFM_Best_PE
unsgn_LFM_Equal_Arch_ME_P25 = LIMComponents.unsgn_LFM_Equal_Arch_ME_P25
unsgn_LFM_Equal_Arch_ME_P50 = LIMComponents.unsgn_LFM_Equal_Arch_ME_P50
unsgn_LFM_Equal_Arch_MSE = LIMComponents.unsgn_LFM_Equal_Arch_MSE
unsgn_LFM_Equal_Arch_PE = LIMComponents.unsgn_LFM_Equal_Arch_PE
unsgn_LFM_ME_0 = LIMComponents.unsgn_LFM_ME_0
unsgn_LFM_ME_N25 = LIMComponents.unsgn_LFM_ME_N25
unsgn_LFM_ME_N50 = LIMComponents.unsgn_LFM_ME_N50
unsgn_LFM_ME_N75 = LIMComponents.unsgn_LFM_ME_N75
unsgn_LFM_ME_P25 = LIMComponents.unsgn_LFM_ME_P25
unsgn_LFM_ME_P50 = LIMComponents.unsgn_LFM_ME_P50
unsgn_LFM_ME_P75 = LIMComponents.unsgn_LFM_ME_P75

COMPONENTS = {
    "lim_best_mae": unsgn_LFM_Best_MAE,
    "lim_best_pe": unsgn_LFM_Best_PE,
    "lim_equal_arch_me_p25": unsgn_LFM_Equal_Arch_ME_P25,
    "lim_equal_arch_me_p50": unsgn_LFM_Equal_Arch_ME_P50,
    "lim_equal_arch_mse": unsgn_LFM_Equal_Arch_MSE,
    "lim_equal_arch_pe": unsgn_LFM_Equal_Arch_PE,
    "lim_me_0": unsgn_LFM_ME_0,
    "lim_me_n25": unsgn_LFM_ME_N25,
    "lim_me_n50": unsgn_LFM_ME_N50,
    "lim_me_n75": unsgn_LFM_ME_N75,
    "lim_me_p25": unsgn_LFM_ME_P25,
    "lim_me_p50": unsgn_LFM_ME_P50,
    "lim_me_p75": unsgn_LFM_ME_P75,
}
