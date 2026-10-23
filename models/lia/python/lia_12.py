"""lia_12: extracted without arithmetic changes from assets/codes/LIAs.ipynb.
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


    def unsgn_LFA_21_21_ME_N50_1(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N50_1 Approximation.
        """
        # Check to see if the inputlength parameter is correct or not
        if input_length <= 0 or lower_part_length > input_length:
            print("Invalid InputLength and LowerPartLength in LSA_Inputs!")
            sys.exit(1)

        # Check to see whether the two inputs are in range or not
        if input1 > (2 ** input_length) - 1 or input1 < 0:
            print("First operand of the LSA Sum is not in range!")
            print(f"Input 1 = {input1}")
            sys.exit(1)
        elif input2 > (2 ** input_length) - 1 or input2 < 0:
            print("Second operand of the LSA Sum is not in range!")
            # Corrected the typo from C where it logged "Input 1 =" for Input2
            print(f"Input 2 = {input2}")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        elif lower_part_length == 1:
            # For LPL=1, 2**(1-1) - 1 = 1 - 1 = 0.
            result_lower = (2 ** (lower_part_length - 1)) - 1
        elif lower_part_length == 2:
            result_lower = 1
        else:
            temp1_lower = LIAComponents.slice_number(input1, 2, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 2, lower_part_length - 1, input_length)

            result_lower = temp1_lower | temp2_lower
            # Multiply by 2 and add 1 effectively shifts left and sets LSB to 1
            result_lower = result_lower * 2 + 1

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # Exact addition for the upper parts
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # --- Specific N50_1 modification logic for ResultLower ---
        if lower_part_length == 1 and ((msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0)):
            result_lower += 2 ** (lower_part_length - 1)

        if lower_part_length > 1 and not ((msb_1 & msb_2) == 1):
            result_lower += 2 ** (lower_part_length - 1)

        # --- Specific N50_1 modification logic for ResultUpper (Carry Generation) ---
        if (msb_1 & msb_2) == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


unsgn_LFA_21_21_ME_N50_1 = LIAComponents.unsgn_LFA_21_21_ME_N50_1
compute = unsgn_LFA_21_21_ME_N50_1
