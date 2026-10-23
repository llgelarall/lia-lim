"""lia_11: extracted without arithmetic changes from assets/codes/LIAs.ipynb.
Validated domain: unsigned N=8, LPL=1..7.
Call compute(a,b,8,lpl).
"""
import sys

class LIAComponents:
    def slice_number(number: int, lower_bit: int, upper_bit: int, number_length: int) -> int:
        """
        Extracts a specific range of bits from a given number.
        Equivalent to the C SliceNumber function.
        """
        # Check to see whether the input is in range or not
        if number > (2 ** number_length) - 1 or number < 0:
            print("Operand of the SliceNumber is not in range!")
            sys.exit(1)

        if lower_bit > number_length or upper_bit > number_length or lower_bit > upper_bit or lower_bit < 0 or upper_bit < 0:
            print("\nLength of the SliceNumber function Operands are not correct!")
            sys.exit(1)

        # In C: div(...).quot is integer division, div(...).rem is modulo.
        temp1 = number // (2 ** (lower_bit - 1))
        temp1 = temp1 % (2 ** (upper_bit - lower_bit + 1))

        return temp1


    def unsgn_add_incWL(a: int, b: int, wl_a: int, wl_b: int) -> int:
        """
        Adds two numbers. Word length arguments are kept for signature compatibility.
        """
        return a + b


    def unsgn_LFA_21_21_ME_P25(Input1: int, Input2: int, InputLength: int, LowerPartLength: int) -> int:

        # Check to see if the inputlength parameter is correct or not
        if InputLength <= 0 or LowerPartLength > InputLength:
            raise ValueError("Invalid InputLength and LowerPartLength in LSA_Inputs!")

        # Check to see whether the two inputs are in range or not
        if Input1 > (2**InputLength) - 1 or Input1 < 0:
            raise ValueError(f"First operand of the LSA Sum is not in range! Input 1 = {Input1}")
        elif Input2 > (2**InputLength) - 1 or Input2 < 0:
            raise ValueError(f"Second operand of the LSA Sum is not in range! Input 2 = {Input2}")

        if LowerPartLength == 0:
            Result = LIAComponents.unsgn_add_incWL(Input1, Input2, InputLength, InputLength)
            return Result

        elif LowerPartLength == 1:
            ResultLower = (2**(LowerPartLength - 1)) - 1

        elif LowerPartLength == 2:
            Temp1Lower = LIAComponents.slice_number(Input1, 1, 1, InputLength)
            Temp2Lower = LIAComponents.slice_number(Input2, 1, 1, InputLength)
            ResultLower = Temp1Lower | Temp2Lower

        else:
            ResultLower = (2**(LowerPartLength - 2)) - 1
            Temp1Lower = LIAComponents.slice_number(Input1, 1, 1, InputLength)
            Temp2Lower = LIAComponents.slice_number(Input2, 1, 1, InputLength)
            ResultLower = ResultLower * 2 + (Temp1Lower | Temp2Lower)

        # Slice the lower and the upper parts of inputs
        Temp1Upper = LIAComponents.slice_number(Input1, LowerPartLength + 1, InputLength, InputLength)
        Temp2Upper = LIAComponents.slice_number(Input2, LowerPartLength + 1, InputLength, InputLength)

        ResultUpper = LIAComponents.unsgn_add_incWL(
            Temp1Upper, Temp2Upper, 
            InputLength - LowerPartLength, 
            InputLength - LowerPartLength
        )

        # Check to see if a possible carry from lower to upper part should be generated or not
        MSB_1 = LIAComponents.slice_number(Input1, LowerPartLength, LowerPartLength, InputLength)
        MSB_2 = LIAComponents.slice_number(Input2, LowerPartLength, LowerPartLength, InputLength)

        # if a carry should be passed, increment the Upper part
        if (MSB_1 == 0 and MSB_2 == 1) or (MSB_1 == 1 and MSB_2 == 0):
            ResultLower += 2**(LowerPartLength - 1)

        if (MSB_1 & MSB_2) == 1:
            ResultUpper = ResultUpper + 1

        # The whole final result is constructed according to the lower and upper parts
        Result = ResultUpper * (2**LowerPartLength) + ResultLower

        return int(Result)


unsgn_LFA_21_21_ME_P25 = LIAComponents.unsgn_LFA_21_21_ME_P25
compute = unsgn_LFA_21_21_ME_P25
