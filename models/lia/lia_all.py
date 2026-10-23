"""All LIA software models. Original notebook arithmetic retained.
Use COMPONENTS[architecture_id](...) or the original class methods.
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

    def unsgn_LFA_21_21_ME_Best(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for Lower Part Approximation (LFA).
        """
        if lower_part_length == input_length:
            result = (2 ** (lower_part_length - 1)) - 1

            msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, lower_part_length)
            msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, lower_part_length)

            if (msb_1 == 1 and msb_2 == 0) or (msb_1 == 0 and msb_2 == 1):
                result += 2 ** (input_length - 1)

            if (msb_1 & msb_2) == 1:
                result += 2 ** input_length

            return result

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
            # Note: Fixed a minor typo from the C code where it said "Input 1 =" for Input 2
            print(f"Input 2 = {input2}") 
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        else:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length, input_length)
            result_lower = (2 ** (lower_part_length - 1)) - 1

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # the upper part should be added two upper parts to produce a correct carry out
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(temp1_lower, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(temp2_lower, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if (msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper = result_upper + 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)



    # Second


    def unsgn_LFA_21_21_MAE_PE_Best(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA MAE PE Best Approximation.
        """
        if lower_part_length == input_length:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result = temp1_lower | temp2_lower

            msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, lower_part_length)
            msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, lower_part_length)

            if (msb_1 == 1 and msb_2 == 0) or (msb_1 == 0 and msb_2 == 1):
                result += 2 ** (input_length - 1)

            if (msb_1 & msb_2) == 1:
                result += 2 ** input_length

            return result

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
            # Fixed the typo from C where it logged "Input 1 =" for Input2
            print(f"Input 2 = {input2}")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        elif lower_part_length == 1:
            result_lower = (2 ** (lower_part_length - 1)) - 1
        else:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # the upper part should be added two upper parts to produce a correct carry out
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if (msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper = result_upper + 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)

    # Third

    def unsgn_LFA_21_21_MSE_Best(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA MSE Best Approximation.
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
            # Fixed the typo from C where it logged "Input 1 =" for Input 2
            print(f"Input 2 = {input2}")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        elif lower_part_length == 1:
            result_lower = (2 ** (lower_part_length - 1)) - 1
        elif lower_part_length == 2 or lower_part_length == 3:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower
        else:
            result_lower = (2 ** (lower_part_length - 3)) - 1

            msb_1 = LIAComponents.slice_number(input1, lower_part_length - 2, lower_part_length - 2, input_length)
            msb_2 = LIAComponents.slice_number(input2, lower_part_length - 2, lower_part_length - 2, input_length)

            if (msb_1 | msb_2) == 1:
                result_lower += 2 ** (lower_part_length - 3)

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if (msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper = result_upper + 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


    # Fourth
    def unsgn_LFA_21_21_MSE_Best_2(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA MSE Best 2 Approximation.
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
            # Fixed the typo from C where it logged "Input 1 =" for Input 2
            print(f"Input 2 = {input2}")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        elif lower_part_length == 1:
            result_lower = (2 ** (lower_part_length - 1)) - 1
        elif lower_part_length == 2:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower
        else:
            result_lower = (2 ** (lower_part_length - 2)) - 1

            msb_1 = LIAComponents.slice_number(input1, lower_part_length - 1, lower_part_length - 1, input_length)
            msb_2 = LIAComponents.slice_number(input2, lower_part_length - 1, lower_part_length - 1, input_length)

            if (msb_1 | msb_2) == 1:
                result_lower += 2 ** (lower_part_length - 2)

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # the upper part should be added two upper parts to produce a correct carry out

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if (msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper = result_upper + 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


    # fifth
    def unsgn_LFA_21_21_ME_0_1(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME 0_1 Approximation.
        """
        # Check to see if the inputlength parameter is correct or not
        if input_length <= 0 or lower_part_length > input_length:
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
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # Adding two lower and upper parts of the inputs individually

        # the lower part is constructed using OR between lower parts of the inputs
        # (Note: the C code simply sets this to the maximum possible value for the lower part length)
        result_lower = (2 ** lower_part_length) - 1

        # the upper part should be added two upper parts to produce a correct carry out
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)

    # sixth
    def unsgn_LFA_21_21_ME_0_2(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME 0_2 Approximation.
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
            # Fixed the typo from C where it logged "Input 1 =" for Input 2
            print(f"Input 2 = {input2}")
            sys.exit(1)

        if lower_part_length == 0:
            result = LIAComponents.unsgn_add_incWL(input1, input2, input_length, input_length)
            return result
        elif lower_part_length == 1:
            result_lower = (2 ** (lower_part_length - 1)) - 1
        elif lower_part_length == 2:
            result_lower = LIAComponents.slice_number(input2, 1, 1, input_length)
        else:
            temp1_lower = LIAComponents.slice_number(input1, 2, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 2, lower_part_length - 1, input_length)

            result_lower = temp1_lower | temp2_lower

            result_lower = result_lower * 2 + LIAComponents.slice_number(input2, 1, 1, input_length)

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # the upper part should be added two upper parts to produce a correct carry out

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if lower_part_length == 1 and ((msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0)):
            result_lower += 2 ** (lower_part_length - 1)

        if lower_part_length > 1 and not ((msb_1 & msb_2) == 1):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper = result_upper + 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)



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

    # seventh
    def unsgn_LFA_21_21_ME_N25_LOA(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N25 LOA Approximation.
        """
        # Check to see if the inputlength parameter is correct or not
        if input_length <= 0 or lower_part_length > input_length:
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

        # the lower part is constructed using OR between lower parts of the inputs
        result_lower = temp1_lower | temp2_lower

        # the upper part should be added two upper parts to produce a correct carry out
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_lower1 = LIAComponents.slice_number(temp1_lower, lower_part_length, lower_part_length, lower_part_length)
        msb_lower2 = LIAComponents.slice_number(temp2_lower, lower_part_length, lower_part_length, lower_part_length)

        # Simulating C's logical AND (&&) which evaluates to an integer 1 or 0
        possible_carry = 1 if (msb_lower1 and msb_lower2) else 0

        # if a carry should be passed, increment the Upper part
        if possible_carry == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)

    # eighth

    def unsgn_LFA_21_21_ME_N25_2(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N25_2 Approximation.
        """
        # Handle the specific case where LowerPartLength equals InputLength first
        if lower_part_length == input_length:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result = temp1_lower | temp2_lower

            msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, lower_part_length)
            msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, lower_part_length)

            if (msb_1 == 1 and msb_2 == 0) or (msb_1 == 0 and msb_2 == 1):
                result += 2 ** (input_length - 1)

            if (msb_1 & msb_2) == 1:
                result += 2 ** input_length

            return int(result)

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
            result_lower = (2 ** (lower_part_length - 1)) - 1
        else:
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # the upper part should be added two upper parts to produce a correct carry out

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if lower_part_length == 1 and ((msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0)):
            result_lower += 2 ** (lower_part_length - 1)

        if lower_part_length > 1 and not ((msb_1 & msb_2) == 1):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


    # nineth

    def unsgn_LFA_21_21_ME_N25_3(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N25_3 Approximation.
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
        else:
            # OR the lower bits, excluding the MSB of the lower part
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower

        # Slice and add the upper parts of inputs exactly
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Extract the MSB of the lower part from each input
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # --- Start of unique adjustment/carry logic for this function ---

        # Adjust the lower part result based on MSBs
        if lower_part_length == 1 and ((msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0)):
            result_lower += 2 ** (lower_part_length - 1)  # Adds 1

        if lower_part_length > 1 and (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        # Adjust the upper part result (carry-in) based on MSBs
        if lower_part_length == 1 and (msb_1 & msb_2) == 1:
            result_upper += 1

        if lower_part_length > 1 and msb_2 == 1:
            result_upper += 1

        # --- End of unique adjustment/carry logic ---

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)



    # tenth
    def unsgn_LFA_21_21_ME_N25_4(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME N25_4 Approximation.
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
        else:
            # OR the lower bits, excluding the MSB of the lower part
            temp1_lower = LIAComponents.slice_number(input1, 1, lower_part_length - 1, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 1, lower_part_length - 1, input_length)
            result_lower = temp1_lower | temp2_lower

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        # Exact addition for the upper parts
        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # --- Specific N25_4 modification logic for ResultLower ---
        if lower_part_length == 1 and ((msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0)):
            result_lower += 2 ** (lower_part_length - 1)

        if lower_part_length > 1 and (msb_1 == 0 and msb_2 == 1):
            result_lower += 2 ** (lower_part_length - 1)

        # --- Specific N25_4 modification logic for ResultUpper (Carry Generation) ---
        if lower_part_length == 1 and (msb_1 & msb_2) == 1:
            result_upper += 1

        if lower_part_length > 1 and msb_1 == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


    def unsgn_LFA_21_21_ME_P50(input1: int, input2: int, input_length: int, lower_part_length: int) -> int:
        """
        Main Logic Function for LFA ME P50 Approximation.
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
            result_lower = (2 ** (lower_part_length - 1)) - 1
        elif lower_part_length == 2:
            result_lower = LIAComponents.slice_number(input2, 1, 1, input_length)
        elif lower_part_length == 3:
            temp1_lower = LIAComponents.slice_number(input1, 2, 2, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 2, 2, input_length)

            result_lower = temp1_lower | temp2_lower
            result_lower = result_lower * 2 + 1
        else:
            temp1_lower = LIAComponents.slice_number(input1, 2, 2, input_length)
            temp2_lower = LIAComponents.slice_number(input2, 2, 2, input_length)

            result_lower = temp1_lower | temp2_lower
            result_lower = result_lower * 2 + 1

            temp1_lower = (2 ** (lower_part_length - 3)) - 1
            result_lower = temp1_lower * 4 + result_lower

        # Slice the lower and the upper parts of inputs
        temp1_upper = LIAComponents.slice_number(input1, lower_part_length + 1, input_length, input_length)
        temp2_upper = LIAComponents.slice_number(input2, lower_part_length + 1, input_length, input_length)

        result_upper = LIAComponents.unsgn_add_incWL(temp1_upper, temp2_upper, input_length - lower_part_length, input_length - lower_part_length)

        # the upper part should be added two upper parts to produce a correct carry out

        # Check to see if a possible carry from lower to upper part should be generated or not
        msb_1 = LIAComponents.slice_number(input1, lower_part_length, lower_part_length, input_length)
        msb_2 = LIAComponents.slice_number(input2, lower_part_length, lower_part_length, input_length)

        # if a carry should be passed, increment the Upper part
        if (msb_1 == 0 and msb_2 == 1) or (msb_1 == 1 and msb_2 == 0):
            result_lower += 2 ** (lower_part_length - 1)

        if (msb_1 & msb_2) == 1:
            result_upper += 1

        # The whole final result is constructed according to the lower and upper parts
        result = result_upper * (2 ** lower_part_length) + result_lower

        return int(result)


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






unsgn_LFA_21_21_ME_Best = LIAComponents.unsgn_LFA_21_21_ME_Best
unsgn_LFA_21_21_MAE_PE_Best = LIAComponents.unsgn_LFA_21_21_MAE_PE_Best
unsgn_LFA_21_21_MSE_Best = LIAComponents.unsgn_LFA_21_21_MSE_Best
unsgn_LFA_21_21_MSE_Best_2 = LIAComponents.unsgn_LFA_21_21_MSE_Best_2
unsgn_LFA_21_21_ME_N50_2 = LIAComponents.unsgn_LFA_21_21_ME_N50_2
unsgn_LFA_21_21_ME_N25_LOA = LIAComponents.unsgn_LFA_21_21_ME_N25_LOA
unsgn_LFA_21_21_ME_N25_2 = LIAComponents.unsgn_LFA_21_21_ME_N25_2
unsgn_LFA_21_21_ME_N25_3 = LIAComponents.unsgn_LFA_21_21_ME_N25_3
unsgn_LFA_21_21_ME_N25_4 = LIAComponents.unsgn_LFA_21_21_ME_N25_4
unsgn_LFA_21_21_ME_0_1 = LIAComponents.unsgn_LFA_21_21_ME_0_1
unsgn_LFA_21_21_ME_0_2 = LIAComponents.unsgn_LFA_21_21_ME_0_2
unsgn_LFA_21_21_ME_P25 = LIAComponents.unsgn_LFA_21_21_ME_P25
unsgn_LFA_21_21_ME_N50_1 = LIAComponents.unsgn_LFA_21_21_ME_N50_1
unsgn_LFA_21_21_ME_P50 = LIAComponents.unsgn_LFA_21_21_ME_P50

COMPONENTS = {
    "lia_00": unsgn_LFA_21_21_ME_Best,
    "lia_01": unsgn_LFA_21_21_MAE_PE_Best,
    "lia_02": unsgn_LFA_21_21_MSE_Best,
    "lia_03": unsgn_LFA_21_21_MSE_Best_2,
    "lia_04": unsgn_LFA_21_21_ME_N50_2,
    "lia_05": unsgn_LFA_21_21_ME_N25_LOA,
    "lia_06": unsgn_LFA_21_21_ME_N25_2,
    "lia_07": unsgn_LFA_21_21_ME_N25_3,
    "lia_08": unsgn_LFA_21_21_ME_N25_4,
    "lia_09": unsgn_LFA_21_21_ME_0_1,
    "lia_10": unsgn_LFA_21_21_ME_0_2,
    "lia_11": unsgn_LFA_21_21_ME_P25,
    "lia_12": unsgn_LFA_21_21_ME_N50_1,
    "lia_13": unsgn_LFA_21_21_ME_P50,
}
