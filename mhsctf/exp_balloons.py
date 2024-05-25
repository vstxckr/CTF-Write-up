from pwn import *

msg = "Tracking number not found!"
rcv = msg
i = 0

while (rcv != msg and i < 2147483647):
    p = remote("0.cloud.chals.io", 34293)
    p.recvline()
    p.recvline()
    p.sendline(str(i).encode('ascii'))
    p.recvline()
    rcv = p.recvline()
    print(rcv)
    i += 1
    p.close()
