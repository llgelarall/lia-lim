/* lia_08: standalone extraction from assets/codes/LFAs.c.
 * Arithmetic function bodies preserved; private helpers have internal linkage.
 * Validated domain: unsigned N=8, LPL=1..7. Link with -lm.
 */
#include <stdlib.h>
#include <stdio.h>
#include <math.h>





/*************************************************
 * ***************** LFA Functions ***************
 * ***********************************************/
//0

//1

//2

//3

//4

//5

//6

//7

//8

///9

//10

//12

//13

//14


/***************************************************
 * *************************************************
 */


static unsigned int SliceNumber(unsigned int Number, unsigned int LowerBit,
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

static unsigned int unsgn_add_incWL(unsigned int a, unsigned int b, unsigned int WL_a,
							 unsigned int WL_b)
{
	return a + b;
}

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
