#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef struct bit
{
    unsigned x:1;
}bit;


unsigned long int unsgn_LFM_Best_PE(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];

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

//	if(VBL-3 > 0)
//	{
//		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
//		sum = (VBL-3)*(C[0].x);
//	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) | (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) ^ (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1 & part_2) >> i;
			else if(i == 1)
				S[i].x = ( (part_1 ^ part_2) ) >> i;
			else
				S[i].x = (part_1 | part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_Best_MAE(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];

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

//	if(VBL-3 > 0)
//	{
//		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
//		sum = (VBL-3)*(C[0].x);
//	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1 & part_2) >> i;
			else if(i == 1)
				S[i].x = ( (part_1 | part_2) ) >> i;
			else
				S[i].x = (part_1 | part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_ME_0(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) | (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) | (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1 | part_2) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_ME_P25(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_ME_P50(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1 & part_2) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}






unsigned long int unsgn_LFM_ME_P75(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = 0;
	}
	else if(VBL == 3)
	{
		S[0].x = 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = 0;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_ME_N25(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) | (op2 & (unsigned long int)(1 << 2)) ) >> 2;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if((i==0) || (i==1))
				S[i].x = (part_1) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_ME_N50(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) | (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = 1;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if((i==0) || (i==1))
				S[i].x = (part_1 & part_2) >> i;
			if(i==2)
				S[i].x = (part_1) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}



unsigned long int unsgn_LFM_ME_N75(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-3 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-3)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) | (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = 1;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			if(i==0)
				S[i].x = (part_1) >> i;
			else if(i==1)
				S[i].x = (part_1 & part_2) >> i;
			else if(i==2)
				S[i].x = (part_1) >> i;
			else if(i == (VBL-1))
				S[i].x = ( ~(part_1 & part_2) ) >> i;
			else
				S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


//============= Equal Architectures ===============

unsigned long int unsgn_LFM_Equal_Arch_PE(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];

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

//	if(VBL-3 > 0)
//	{
//		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
//		sum = (VBL-3)*(C[0].x);
//	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) & (op2 & (unsigned long int)(1 << 2)) ) >> 2;;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


unsigned long int unsgn_LFM_Equal_Arch_MSE(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];

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

//	if(VBL-3 > 0)
//	{
//		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
//		sum = (VBL-3)*(C[0].x);
//	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0))  ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1))  ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2))  ) >> 2;;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			S[i].x = (part_1 | part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}


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


unsigned long int unsgn_LFM_Equal_Arch_ME_P50(unsigned long int op1, unsigned long int op2, int WL1, int WL2, int VBL)
{
	int i;
	unsigned long int number2;
	unsigned long int sum = 0;
	unsigned long int imprecise_part = 0;
	unsigned long int part_1 , part_2;

	number2 = op2;

	int PP[WL2];
	bit S[WL2];
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

	if(VBL-2 > 0)
	{
		C[0].x = ( ((op1 & (unsigned long int)(1<< (VBL-1))) & (op2 & (unsigned long int)(1 << (VBL-1)))) >> (VBL-1) ) ;
		sum = (VBL-2)*(C[0].x);
	}

	for (i = 0; i < WL2; i++)
		sum = sum + PP[i];

	sum = sum*pow(2,VBL);

	if(VBL == 1)
		S[0].x = 0;
	if(VBL == 2)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
	}
	else if(VBL == 3)
	{
		S[0].x = ( (op1 & (unsigned long int)(1<< 0)) & (op2 & (unsigned long int)(1 << 0)) ) >> 0;
		S[1].x = ( (op1 & (unsigned long int)(1<< 1)) & (op2 & (unsigned long int)(1 << 1)) ) >> 1;
		S[2].x = ( (op1 & (unsigned long int)(1<< 2)) & (op2 & (unsigned long int)(1 << 2)) ) >> 2;;
	}
	else if(VBL > 3)
	{
		for(i=0; i<VBL; i++)
		{
			part_1 = (op1 & (unsigned long int)(1 << i));
			part_2 = (op2 & (unsigned long int)(1 << i));
			S[i].x = (part_1 & part_2) >> i;
		}
	}

	for(i=0; i<VBL; i++)
		imprecise_part += S[i].x*pow(2,i);

	sum += imprecise_part;

	return sum;
}