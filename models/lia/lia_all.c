#include <stdlib.h>
#include <stdio.h>
#include <math.h>

unsigned int SliceNumber(unsigned int Number, unsigned int LowerBit,
						 unsigned int UpperBit, unsigned int NumberLength)
{
	unsigned int Temp1;
	// printf("here");
	char str[256];
	// Check to see weather the input is in range or not
	if ((Number > pow(2, NumberLength) - 1) || (Number < 0))
	{
		printf("Operand of the SliceNumber is not in range!\n");
		exit(1);
	}
	if ((LowerBit > NumberLength) || (UpperBit > NumberLength) || (LowerBit > UpperBit) || (LowerBit < 0) || (UpperBit < 0))
	{
		printf("\nLength of the SliceNumber function Operands are not correct!\n");
		exit(1);
	}

	Temp1 = div(Number, (unsigned int)pow(2, LowerBit - 1)).quot;
	Temp1 = div(Temp1, (unsigned int)pow(2, UpperBit - LowerBit + 1)).rem;
	return Temp1;
}

unsigned int unsgn_add_incWL(unsigned int a, unsigned int b, unsigned int WL_a,
							 unsigned int WL_b)
{
	return a + b;
}

/*************************************************
 * ***************** LFA Functions ***************
 * ***********************************************/
//0
unsigned int unsgn_LFA_21_21_ME_Best(unsigned int Input1, unsigned int Input2,
									 unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	if (LowerPartLength == InputLength)
	{
		Result = pow(2, LowerPartLength - 1) - 1;

		MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
							LowerPartLength);
		MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
							LowerPartLength);

		if (((MSB_1 == 1) && (MSB_2 == 0)) || (((MSB_1 == 0) && (MSB_2 == 1))))
		{

			Result += pow(2, InputLength - 1);
		}

		if ((MSB_1 & MSB_2) == 1)
		{

			Result += pow(2, InputLength);
		}
		return Result;
	}

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength, InputLength);
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);

	// the upper part should be added two upper parts to produce a correct carry out
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Temp1Lower, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Temp2Lower, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}

	if ((MSB_1 & MSB_2) == 1)
	{
		ResultUpper = ResultUpper + 1;
	}

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//1
unsigned int unsgn_LFA_21_21_MAE_PE_Best(unsigned int Input1, unsigned int Input2,
										 unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	if (LowerPartLength == InputLength)
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		Result = Temp1Lower | Temp2Lower;

		MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
							LowerPartLength);
		MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
							LowerPartLength);

		if (((MSB_1 == 1) && (MSB_2 == 0)) || (((MSB_1 == 0) && (MSB_2 == 1))))
		{

			Result += pow(2, InputLength - 1);
		}

		if ((MSB_1 & MSB_2) == 1)
		{

			Result += pow(2, InputLength);
		}
		return Result;
	}

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//2
unsigned int unsgn_LFA_21_21_MSE_Best(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2) || (LowerPartLength == 3))
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}
	else
	{
		ResultLower = pow(2, LowerPartLength - 3) - 1;

		MSB_1 = SliceNumber(Input1, LowerPartLength - 2, LowerPartLength - 2,
							InputLength);
		MSB_2 = SliceNumber(Input2, LowerPartLength - 2, LowerPartLength - 2,
							InputLength);
		if ((MSB_1 | MSB_2) == 1)
			ResultLower += pow(2, LowerPartLength - 3);
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//3
unsigned int unsgn_LFA_21_21_MSE_Best_2(unsigned int Input1, unsigned int Input2,
										unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2))
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}
	else
	{
		ResultLower = pow(2, LowerPartLength - 2) - 1;

		MSB_1 = SliceNumber(Input1, LowerPartLength - 1, LowerPartLength - 1,
							InputLength);
		MSB_2 = SliceNumber(Input2, LowerPartLength - 1, LowerPartLength - 1,
							InputLength);
		if ((MSB_1 | MSB_2) == 1)
			ResultLower += pow(2, LowerPartLength - 2);
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//4
unsigned int unsgn_LFA_21_21_ME_0_1(unsigned int Input1, unsigned int Input2,
									unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LORAdder_Signed_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);
	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);

	// Adding two lower and upper parts of the inputs individually

	// the lower part is constructed using OR between lower parts of the inputs
	ResultLower = pow(2, LowerPartLength) - 1;
	// the upper part should be added two upper parts to produce a correct carry out
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// Check to see if a possible carry from lower to upper part should be generated or not

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//5
unsigned int unsgn_LFA_21_21_ME_0_2(unsigned int Input1, unsigned int Input2,
									unsigned int InputLength, unsigned int LowerPartLength)
{
	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2))
	{
		ResultLower = SliceNumber(Input2, 1, 1, InputLength);
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 2, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 2, LowerPartLength - 1, InputLength);

		ResultLower = Temp1Lower | Temp2Lower;

		ResultLower = ResultLower * 2 + SliceNumber(Input2, 1, 1, InputLength);
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if ((LowerPartLength == 1) && (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((LowerPartLength > 1) && (!((MSB_1 & MSB_2) == 1)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//6
unsigned int unsgn_LFA_21_21_ME_P25(unsigned int Input1, unsigned int Input2,
									unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2))
	{
		Temp1Lower = SliceNumber(Input1, 1, 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}
	else
	{

		ResultLower = pow(2, LowerPartLength - 2) - 1;

		Temp1Lower = SliceNumber(Input1, 1, 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, 1, InputLength);

		ResultLower = ResultLower * 2 + (Temp1Lower | Temp2Lower);
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//7
unsigned int unsgn_LFA_21_21_ME_N25_LOA(unsigned int Input1, unsigned int Input2,
										unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	unsigned int PossibleCarry;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LORAdder_Signed_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}

	// Slice the lower and the upper parts of inputs
	Temp1Lower = SliceNumber(Input1, 1, LowerPartLength, InputLength);
	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);
	Temp2Lower = SliceNumber(Input2, 1, LowerPartLength, InputLength);
	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);

	// Adding two lower and upper parts of the inputs individually

	// the lower part is constructed using OR between lower parts of the inputs
	ResultLower = Temp1Lower | Temp2Lower;
	// the upper part should be added two upper parts to produce a correct carry out
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// Check to see if a possible carry from lower to upper part should be generated or not
	PossibleCarry = SliceNumber(Temp1Lower, LowerPartLength, LowerPartLength,
								LowerPartLength) &&
					SliceNumber(Temp2Lower, LowerPartLength, LowerPartLength,
								LowerPartLength);

	// if a carry should be passed, increment the Upper part
	if (PossibleCarry == 1)
	{
		ResultUpper++;
		//		if (ResultUpper > (pow(2, InputLength - LowerPartLength + 1) - 1))
		//			ResultUpper = ResultUpper
		//					- (long int) pow(2, InputLength - LowerPartLength + 1);
	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//8
unsigned int unsgn_LFA_21_21_ME_N25_2(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	if (LowerPartLength == InputLength)
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		Result = Temp1Lower | Temp2Lower;

		MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
							LowerPartLength);
		MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
							LowerPartLength);

		if (((MSB_1 == 1) && (MSB_2 == 0)) || (((MSB_1 == 0) && (MSB_2 == 1))))
		{

			Result += pow(2, InputLength - 1);
		}

		if ((MSB_1 & MSB_2) == 1)
		{

			Result += pow(2, InputLength);
		}
		return Result;
	}

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {

	if ((LowerPartLength == 1) && (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((LowerPartLength > 1) && (!((MSB_1 & MSB_2) == 1)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
///9
unsigned int unsgn_LFA_21_21_ME_N25_3(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {

	if ((LowerPartLength == 1) && (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((LowerPartLength > 1) && ((MSB_1 == 1) && (MSB_2 == 0)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((LowerPartLength == 1) && ((MSB_1 & MSB_2) == 1))
		ResultUpper = ResultUpper + 1;

	if ((LowerPartLength > 1) && (MSB_2 == 1))
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//10
unsigned int unsgn_LFA_21_21_ME_N25_4(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 1, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 1, LowerPartLength - 1, InputLength);
		ResultLower = Temp1Lower | Temp2Lower;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {

	if ((LowerPartLength == 1) && (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((LowerPartLength > 1) && ((MSB_1 == 0) && (MSB_2 == 1)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((LowerPartLength == 1) && ((MSB_1 & MSB_2) == 1))
		ResultUpper = ResultUpper + 1;

	if ((LowerPartLength > 1) && (MSB_1 == 1))
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//12
unsigned int unsgn_LFA_21_21_ME_P50(unsigned int Input1, unsigned int Input2,
									unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2))
	{
		ResultLower = SliceNumber(Input2, 1, 1, InputLength);
	}
	else if (LowerPartLength == 3)
	{
		Temp1Lower = SliceNumber(Input1, 2, 2, InputLength);
		Temp2Lower = SliceNumber(Input2, 2, 2, InputLength);

		ResultLower = Temp1Lower | Temp2Lower;

		ResultLower = ResultLower * 2 + 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 2, 2, InputLength);
		Temp2Lower = SliceNumber(Input2, 2, 2, InputLength);

		ResultLower = Temp1Lower | Temp2Lower;

		ResultLower = ResultLower * 2 + 1;

		Temp1Lower = pow(2, LowerPartLength - 3) - 1;

		ResultLower = Temp1Lower * 4 + ResultLower;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if ((((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//13
unsigned int unsgn_LFA_21_21_ME_N50_1(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	//	unsigned int PossibleCarry;
	unsigned int MSB_1, MSB_2;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LSA_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input1);
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the LSA Sum is not in range!\n");
		printf("Input 1 = %u", Input2);
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}
	else if (LowerPartLength == 1)
	{
		ResultLower = pow(2, LowerPartLength - 1) - 1;
	}
	else if ((LowerPartLength == 2))
	{
		ResultLower = 1;
	}
	else
	{
		Temp1Lower = SliceNumber(Input1, 2, LowerPartLength - 1, InputLength);
		Temp2Lower = SliceNumber(Input2, 2, LowerPartLength - 1, InputLength);

		ResultLower = Temp1Lower | Temp2Lower;

		ResultLower = ResultLower * 2 + 1;
	}

	// Slice the lower and the upper parts of inputs

	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);

	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// the upper part should be added two upper parts to produce a correct carry out

	// Check to see if a possible carry from lower to upper part should be generated or not
	MSB_1 = SliceNumber(Input1, LowerPartLength, LowerPartLength,
						InputLength);
	MSB_2 = SliceNumber(Input2, LowerPartLength, LowerPartLength,
						InputLength);

	// if a carry should be passed, increment the Upper part
	//	if ((MSB_1 == 0) && (MSB_2 == 0) ) {
	if ((LowerPartLength == 1) && (((MSB_1 == 0) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))))
		ResultLower += pow(2, LowerPartLength - 1);

	if ((LowerPartLength > 1) && (!((MSB_1 & MSB_2) == 1)))
		ResultLower += pow(2, LowerPartLength - 1);

	//	}
	if ((MSB_1 & MSB_2) == 1)
		ResultUpper = ResultUpper + 1;

	//	if (((MSB_1 == 1) && (MSB_2 == 1)) || ((MSB_1 == 1) && (MSB_2 == 0))) {
	//			ResultUpper = ResultUpper + 1;
	//	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}
//14
unsigned int unsgn_LFA_21_21_ME_N50_2(unsigned int Input1, unsigned int Input2,
									  unsigned int InputLength, unsigned int LowerPartLength)
{

	unsigned int Temp1Lower, Temp2Lower, Temp1Upper, Temp2Upper, ResultLower,
		ResultUpper, Result;
	unsigned int PossibleCarry;

	// Check to see if the inputlength parameter is correct or not
	if (InputLength <= 0 || LowerPartLength > InputLength)
	{
		printf(
			"Invalid InputLength and LowerPartLength in LORAdder_Signed_Inputs!\n");
		// getch();
		exit(1);
	}

	// Check to see weather the two inputs are in range or not
	if ((Input1 > pow(2, InputLength) - 1) || (Input1 < 0))
	{
		printf(
			"First operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}
	else if ((Input2 > pow(2, InputLength) - 1) || (Input2 < 0))
	{
		printf(
			"Second operand of the CAS Signed Twos Complement Sum is not in range!\n");
		// getch();
		exit(1);
	}

	if (LowerPartLength == 0)
	{
		Result = unsgn_add_incWL(Input1, Input2, InputLength, InputLength);
		return Result;
	}

	// Slice the lower and the upper parts of inputs
	Temp1Lower = SliceNumber(Input1, 1, LowerPartLength, InputLength);
	Temp1Upper = SliceNumber(Input1, LowerPartLength + 1, InputLength,
							 InputLength);
	Temp2Lower = SliceNumber(Input2, 1, LowerPartLength, InputLength);
	Temp2Upper = SliceNumber(Input2, LowerPartLength + 1, InputLength,
							 InputLength);

	// Adding two lower and upper parts of the inputs individually

	// the lower part is constructed using OR between lower parts of the inputs
	ResultLower = Temp1Lower;
	// the upper part should be added two upper parts to produce a correct carry out
	ResultUpper = unsgn_add_incWL(Temp1Upper, Temp2Upper, InputLength - LowerPartLength, InputLength - LowerPartLength);

	// Check to see if a possible carry from lower to upper part should be generated or not
	PossibleCarry = SliceNumber(Temp2Lower, LowerPartLength, LowerPartLength,
								LowerPartLength);

	// if a carry should be passed, increment the Upper part
	if (PossibleCarry == 1)
	{
		ResultUpper++;
	}

	// The whole final result is constructed according to the lower and upper parts
	Result = ResultUpper * (long int)pow(2, LowerPartLength) + ResultLower;

	return Result;
}

/***************************************************
 * *************************************************
 */
