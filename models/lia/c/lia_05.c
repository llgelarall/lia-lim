/* lia_05: standalone extraction from assets/codes/LFAs.c.
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
