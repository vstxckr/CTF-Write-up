#include<stdio.h>
#include<string.h>

int main()
{

	unsigned char output[] =
	{
	  0x63, 0xCB, 0xD7, 0xD4, 0xCD, 0x26, 0x15, 0x56, 0x96, 0x64, 
	  0xF4, 0x3A, 0x46, 0xB0, 0xEB, 0x9E, 0x3E, 0xB3, 0x36, 0x21, 
	  0xE4, 0x08, 0x96, 0xD1, 0xC5, 0x43, 0x4B, 0x8C, 0x1A, 0x0C, 
	  0x78, 0xA8, 0xE8, 0xF6, 0x37, 0x3C, 0x0C, 0x98, 0x9C, 0x23, 
	  0xD1, 0xF2, 0x50, 0x91, 0x09, 0xA1, 0x22, 0x59, 0x66, 0x53, 
	  0x68, 0x36, 0xBB, 0x53, 0x25, 0xAE, 0xAC, 0xEE, 0x84, 0xDE, 
	  0x82, 0xB7, 0xDA, 0x38, 0xFB, 0x0B, 0xE5, 0xE4, 0xB2, 0x43, 
	  0xC8, 0xEF, 0xD4, 0x8B, 0xDC, 0x36, 0xBF, 0xD0, 0x0D, 0xF2, 
	  0x85, 0x15, 0x11, 0xCD, 0x7B, 0x62, 0xB8, 0x77, 0xFE, 0xDD, 
	  0xF6, 0x9A, 0xE4, 0xB8, 0xC7, 0xFF, 0xB5, 0xB7, 0x63, 0x38, 
	  0xB4, 0x49, 0xD2, 0xF2, 0x77, 0xD7, 0xA5, 0x19, 0xA5, 0xC3, 
	  0x73, 0xB3, 0x8E, 0xD0, 0x35, 0x79, 0x9C, 0x17, 0x30, 0xC2, 
	  0x3F, 0x36, 0xD9, 0x39, 0x2A, 0x7F, 0x83, 0x20, 0xE6
	};
	unsigned char dat[] =
	{
	  0x78, 0xCF, 0xC4, 0x85, 0xDC, 0x33, 0x07, 0x4C, 0x93, 0x35, 
	  0xFB, 0x7C, 0x10, 0x8E, 0xBE, 0x93, 0x28, 0xE6, 0x2E, 0x75, 
	  0xDA, 0x5E, 0x85, 0xC5, 0x91, 0x15, 0x75, 0x89, 0x48, 0x0E, 
	  0x29, 0xA4, 0xF9, 0xA6, 0x3A, 0x6E, 0x1F, 0x84, 0xF7, 0x42, 
	  0xB0, 0x93, 0x31, 0xF0, 0x68, 0xC0, 0x43, 0x38, 0x07, 0x32, 
	  0x09, 0x57, 0xDA, 0x32, 0x44, 0xCF, 0xCD, 0x8F, 0xE5, 0xBF, 
	  0xE3, 0xD6, 0xBB, 0x59, 0x9A, 0x6A, 0x84, 0x85, 0xD3, 0x22, 
	  0xA9, 0x8E, 0xB5, 0xEA, 0xBD, 0x57, 0xDE, 0xB1, 0x6C, 0x93, 
	  0xE4, 0x74, 0x70, 0xAC, 0x1A, 0x03, 0xD9, 0x16, 0x9F, 0xBC, 
	  0x97, 0xFB, 0x85, 0xD9, 0xA6, 0x9E, 0xD4, 0xD6, 0x02, 0x59, 
	  0xD5, 0x28, 0xB3, 0x93, 0x16, 0xB6, 0xC4, 0x78, 0xC4, 0xA2, 
	  0x12, 0xD2, 0xEF, 0xB1, 0x54, 0x18, 0xFD, 0x76, 0x51, 0xA3, 
	  0x5E, 0x57, 0xB8, 0x58, 0x4B, 0x1E, 0xE2, 0x41
	};


	for ( int i = 0 ; i < 128 ; i++ )
	{
		printf("%c", (output[i] ^ dat[i] ^ 'a'));
	}
}
