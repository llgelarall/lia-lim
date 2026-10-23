/* lim_equal_arch_me_p25: standalone extraction from assets/codes/LFMs.c.
 * Arithmetic function bodies preserved; private helpers have internal linkage.
 * Validated domain: unsigned N=8, LPL=1..7. Link with -lm.
 */
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef struct bit
{
    unsigned x:1;
}bit;


































//============= Equal Architectures ===============














unsigned long int unsgn_LFM_Equal_Arch_ME_P25(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
//	unsigned long int imprecise_part = 0;
//	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
//	bit S[WL2];
	bit C[WL2];

	for (i = 0; i < WL2; i++)
	{
		PP[i] = (number2 % 2) * op1;
		number2 = number2 / 2;
	}

	for (i = 0; i < WL2; i++)
	{
		PP[i] = PP[i] * pow(2,i);
	}

	for (i = 0; i < WL2; i++)
	{
		PP[i] = PP[i] >> (VBL);
	}

	if(VBL > 1)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-1)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	return sum;
}
