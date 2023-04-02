#! /usr/bin/python3
#  filename: exp6.py

from pwn import *

table = string.ascii_uppercase

res = []

for i in table:
    for j in table:
        for k in table:
            elf = ELF("./babyRE")
            p = elf.process()

            feed = "A"*15 + i+j+k

            p.sendline(feed.encode())

            s = p.recvall()

            if ("Correct" in str(s)):
                log.info("CORRECT WITH " + str(feed) + '\n')
                res.append(feed)

print(res)
