#! /usr/bin/python3
#  filename: exp.py

from pwn import *

table = string.ascii_uppercase

for i in table:
    for j in table:
        for k in table:
            elf = ELF("./babyRE")
            p = elf.process()

            feed = i+j+k

            p.sendline(feed.encode())

            s = p.recvall()

            if ("Correct" in str(s)):
                log.info("CORRECT WITH " + str(feed) + '\n')
                exit()
