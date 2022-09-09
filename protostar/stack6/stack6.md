# Stack 6

## Source Code:

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);                            // <- this function cause buffer overflow    (1)

  ret = __builtin_return_address(0);

  if((ret & 0xbf000000) == 0xbf000000) {   // <- check if the ret of getpath() is on the stack     (2)
    printf("bzzzt (%p)\n", ret);           //          if true, then "bzzzt" and exit with signal 1    (3)
    _exit(1);
  }

  printf("got path %s\n", buffer);         // <-       if false, then it's simply print got path  (4)
}

int main(int argc, char **argv)
{
  getpath();
}
```

## Overview & Main Idea

- This challenge has no-pie, no stack protector, rwx segment.

![img](/assets/checksec.png)

- At first, we can see that the program has buffer overflow vulnerability (1), so we can overwrite on the stack. But we can't overwrite getpath()'s address to another address on the stack that allow us to return to, so we can't use return to shellcode on stack to take control of target.
 
![img](/protostar/stack6/assets/stack_segment.png)

> ## Note: the stack has start at 0xbffeb000 and end at 0xc0000000, so we can't overwrite ret and return on the stack.

- With some informations above, I'll take advantage of ret-to-libc vulnerability to this challenge. 

## Details

### A bit about Ret-to-libc

#### What is Ret-to-libc?

- Ret-to-libc attack (return to libc, or return to C library) is one in which the attacker does not require any shellcode to take control of the target, vulnerability of process. Ret2libc is used to exploit buffer overflow vulnerabilities on systems where stack memory is protected with NX (no execute bit).
- In a standard stack-based buffer overflow, an attacker writes their shellcode into the vulnerable program's stack and executes it on the stack. 
- However, if the vulnerable program's stack is protected (NX bit is set, which is the case on newer systems), attackers can no longer execute their shellcode from the vulnerable program's stack. 
- To fight the NX protection, a return-to-libc technique is used, which enables attackers to bypass the NX bit protection and subvert the vulnerable program's execution flow by re-using existing executable code from the standard C library shared object (/lib/i386-linux-gnu/libc-*.so), that is already loaded and mapped into the vulnerable program's virtual memory space, similarly like ntdll.dll is loaded to all Windows programs.

#### Libc

- Every time you write a C program, you use one or the other of the inbuilt functions, like printf, scanf, puts etc. All the standard C functions have been compiled into a single file, named the standard C library or the libc. A libc is native to the system that you are working on and is independent of the binary (compiled program). You can use the **ldd** command to find out which libc is being used by an application.

![img](/protostar/stack6/assets/ldd.png)

- At a high level, ret-to-libc technique is similar to the regular stack overflow attack, but with one key difference - instead of overwritting the return address of the vulnerable function with address of the shellcode when exploiting a regular stack-based overflow with no stack protection, in ret-to-libc case, the return address is overwritten with a memory address that points to the function system(const char *command) that lives in the libc library, so that when the overflowed function returns, the vulnerable program is forced to jump to the system() function and execute the shell command that was passed to the system() function as the *command argument as part of the supplied shellcode. 
- In our case, we will want the vulnerable program to spawn the /bin/sh shell, so we will make the vulnerable program call system("/bin/sh").

#### The idea of Ret2libc is shown by below image

![img](/protostar/stack6/assets/illustrate_img.png)

### Exploit

