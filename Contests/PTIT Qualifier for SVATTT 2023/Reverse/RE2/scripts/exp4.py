from pwn import *

table = string.ascii_uppercase

res = []
for i in reversed(table):
    for j in reversed(table):
        for k in reversed(table):
            elf = ELF("./babyRE")
            p = elf.process()

            feed = "A"*9 + i+j+k

            p.sendline(feed.encode())

            s = p.recvall()

            if ("Correct" in str(s)):
                log.info("CORRECT WITH" + str(feed) + '\n')
                res.append(feed)
                if (feed == "LAD"):
                    print(res)
                    exit()
print(res)
