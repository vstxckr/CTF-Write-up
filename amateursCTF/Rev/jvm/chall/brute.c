#include<stdio.h>

int main()
{
	for (char i = 32 ; i <= 126 ; i++ )
	{
		printf(" - %c", i);
		char s[100];
		if (i == 34 || i == 92)
			sprintf(s, "echo \"amateursCTF{wh4t_d0_yoU_m34n_j4v4_isnt_\\%c_vm?}\" | java JVM code.jvm", i);
		else	
			sprintf(s, "echo \"amateursCTF{wh4t_d0_yoU_m34n_j4v4_isnt_%c_vm?}\" | java JVM code.jvm", i);
		system(s);
		printf("\n");	
	}
	
}
