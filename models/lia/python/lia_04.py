"""lia_04: extracted without arithmetic changes from assets/codes/LIAs.ipynb.
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


    def unsgn_LFA_21_21_ME_N50_2(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N50_2 Approximation.
        """
        # Check to see if the inputlength parameter is correct or not
        if input_length <= 0 or lower_part_length > input_length:
            # Note: Preserving the exact error message from the C source code
            print("Invalid InputLength and LowerPartLength in LORAdder_Signed_Inputs!")
            sys.exit(1)

        # Check to see whether the two inputs are in range or not
        if input1 > (2 ** input_length) - 1 or input1 < 0:
            print("First operand of the CAS Signed Twos Complement Sum is not in range!")
            sys.exit(1)
        elif input2 > (2 ** input_length) - 1 or input2 < 0:
            print("Second operand of the CAS Signed Twos Complement Sum is not in range!")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result

        # Slice the lower and the upper parts of inputs
        temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length, input_length)
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)

        temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # Adding two lower and upper parts of the inputs individually

        # The lower part is constructed (Note: The C comment says OR, but the C code strictly assigns Temp1Lower)
        result_lower = temp1_lower

        # The upper part should be added two upper parts to produce a correct carry out
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        possible_carry = LIAComponents.slice_number(temp2_lower, lower_part_length, lower_part_length, lower_part_length)

        # if a carry should be passed, increment the Upper part
        if possible_carry == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


unsgn_LFA_21_21_ME_N50_2 = LIAComponents.unsgn_LFA_21_21_ME_N50_2
compute = unsgn_LFA_21_21_ME_N50_2
