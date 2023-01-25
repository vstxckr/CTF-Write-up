# SEED SPRING

## OVERVIEW & IDEA

- This challenge gives us a 32-bit binary file, its infomations and disassembly of main is at bellow.

```
λ ~/seed-sPRiNG/ file seed_spring

seed_spring: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=7df253108e1bd837fb708dfaab20362525740ccd, not stripped

λ ~/seed-sPRiNG/ checksec --file=seed_spring

[*] '~/seed-sPRiNG/seed_spring'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+0h] [ebp-18h] BYREF
  int v5; // [esp+4h] [ebp-14h]
  unsigned int seed; // [esp+8h] [ebp-10h]
  int i; // [esp+Ch] [ebp-Ch]
  int *p_argc; // [esp+10h] [ebp-8h]

  p_argc = &argc;
  puts((const char *)&unk_A50);
  puts((const char *)&unk_A50);
  puts("                                                                             ");
  puts("                          #                mmmmm  mmmmm    \"    mm   m   mmm ");
  puts("  mmm    mmm    mmm    mmm#          mmm   #   \"# #   \"# mmm    #\"m  # m\"   \"");
  puts(" #   \"  #\"  #  #\"  #  #\" \"#         #   \"  #mmm#\" #mmmm\"   #    # #m # #   mm");
  puts("  \"\"\"m  #\"\"\"\"  #\"\"\"\"  #   #          \"\"\"m  #      #   \"m   #    #  # # #    #");
  puts(" \"mmm\"  \"#mm\"  \"#mm\"  \"#m##         \"mmm\"  #      #    \" mm#mm  #   ##  \"mmm\"");
  puts("                                                                             ");
  puts((const char *)&unk_A50);
  puts((const char *)&unk_A50);
  puts("Welcome! The game is easy: you jump on a sPRiNG.");
  puts("How high will you fly?");
  puts((const char *)&unk_A50);
  fflush(stdout);
  seed = time(0);
  srand(seed);
  for ( i = 1; i <= 30; ++i )
  {
    printf("LEVEL (%d/30)\n", i);
    puts((const char *)&unk_A50);
    LOBYTE(v5) = rand() & 0xF;
    v5 = (unsigned __int8)v5;
    printf("Guess the height: ");
    fflush(stdout);
    __isoc99_scanf("%d", &v4);
    fflush(stdin);
    if ( v5 != v4 )
    {
      puts("WRONG! Sorry, better luck next time!");
      fflush(stdout);
      exit(-1);
    }
  }
  puts("Congratulation! You've won! Here is your flag:\n");
  fflush(stdout);
  get_flag();
  fflush(stdout);
  return 0;
}
```

- `main()` functions just puts the banner, then it has 30 times to generate random integer and check that low 4-bits random int with user input, if we can pass through this loop check, we can get into the print flag section.

- `rand()` in c use an algorithm to generate a series of `pseudo-random number`. The `pseudo-random number` means that we can know that series of `pseudo-random number` if we know how it works.

- `rand()` just use a `seed` to create the start point for series of `pseudo-random number`. We can set the `seed` with `srand()` function. So, if we know the `seed`, we can create that series of `pseudo-random number.

> - The  random()  function  uses  a  nonlinear  additive feedback random number generator employing a default table of size 31 long integers to return successive pseudo-random numbers in the range from 0 to 2^31 - 1.  The period of this random number generator is very large, approximately 16 * ((2^31) - 1).
> - The srandom() function sets its argument as the seed for a new sequence of pseudo-random integers to be returned by random().  These sequences are  repeatable by calling srandom() with the same seed value.  If no seed value is provided, the random() function is automatically seeded with a value of 1.

- The program use `time(0)` that is current time since `01/01/1970` measured in seconds. Details of this functions is at bellow.

> ### **time_t time( time_t \*arg );**
> Returns the current calendar time encoded as a time_t object, and also stores it in the time_t object pointed to by arg (unless arg is a null pointer)

- So the idea is first, I check the time of the server, ensure time of us and server are the same. Then I create the program to take the time and set the `seed` for `rand()`, then print the `rand() & 0xf` one by one to feed the server input.

## DETAILS

- First, I check the region and time of this domain

```
λ ~/Desktop/CTF/pwn/ ping jupiter.challenges.picoctf.org
PING jupiter.challenges.picoctf.org (3.131.60.8) 56(84) bytes of data.
^C
--- jupiter.challenges.picoctf.org ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2047ms

λ ~/Desktop/CTF/pwn/ nc 3.131.60.8 8311


                                                                             
                          #                mmmmm  mmmmm    "    mm   m   mmm 
  mmm    mmm    mmm    mmm#          mmm   #   "# #   "# mmm    #"m  # m"   "
 #   "  #"  #  #"  #  #" "#         #   "  #mmm#" #mmmm"   #    # #m # #   mm
  """m  #""""  #""""  #   #          """m  #      #   "m   #    #  # # #    #
 "mmm"  "#mm"  "#mm"  "#m##         "mmm"  #      #    " mm#mm  #   ##  "mmm"
                                                                             
.
.
.
```

- And its time region

![img](/picoCTF/seed_sPRiNG/assets/server.png)

- Then I change the time region of my system

```
λ ~/Desktop/CTF/pwn/ timedatectl set-timezone America/New_York 
λ ~/Desktop/CTF/pwn/ timedatectl
               Local time: Wed 2023-01-25 02:37:22 EST  
           Universal time: Wed 2023-01-25 07:37:22 UTC  
                 RTC time: Wed 2023-01-25 07:37:22      
                Time zone: America/New_York (EST, -0500)
System clock synchronized: no                           
              NTP service: inactive                     
          RTC in local TZ: no
```

- The program I will use to feed the input will look like this.

```c
#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<unistd.h>

int main()
{
  srand(time(0));
  for ( int i = 0 ; i < 30 ; i++ )
  {
      printf("%d\n", rand() & 0xf);
  }
}
```

- And run this bash command, we failed.

```
λ ~/Desktop/CTF/pwn/ ./input | nc 3.131.60.8 8311


                                                                             
                          #                mmmmm  mmmmm    "    mm   m   mmm 
  mmm    mmm    mmm    mmm#          mmm   #   "# #   "# mmm    #"m  # m"   "
 #   "  #"  #  #"  #  #" "#         #   "  #mmm#" #mmmm"   #    # #m # #   mm
  """m  #""""  #""""  #   #          """m  #      #   "m   #    #  # # #    #
 "mmm"  "#mm"  "#mm"  "#m##         "mmm"  #      #    " mm#mm  #   ##  "mmm"
                                                                             


Welcome! The game is easy: you jump on a sPRiNG.
How high will you fly?

LEVEL (1/30)

Guess the height: WRONG! Sorry, better luck next time!
```

- I think when connect to the server, it takes some delay times then the `time(0)` in server and the `time(0)` in my system run in different time. So I create a `sleep(1)` that will delay `1 second` in my system before run the `time(0)`. And it works with some tries.

## EXPLOIT

```c
/*
filename: input.c
gcc -o input input.c
*/
#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<unistd.h>

int main()
{
	sleep(1);
	srand(time(0));
	for ( int i = 0 ; i < 30 ; i++ )
	{
		printf("%d\n", rand() & 0xf);
	}
}
```

```
./input | nc jupiter.challenges.picoctf.org 8311
```

## RESULT

```
λ ~/Desktop/CTF/pwn/ ./input | nc jupiter.challenges.picoctf.org 8311


                                                                             
                          #                mmmmm  mmmmm    "    mm   m   mmm 
  mmm    mmm    mmm    mmm#          mmm   #   "# #   "# mmm    #"m  # m"   "
 #   "  #"  #  #"  #  #" "#         #   "  #mmm#" #mmmm"   #    # #m # #   mm
  """m  #""""  #""""  #   #          """m  #      #   "m   #    #  # # #    #
 "mmm"  "#mm"  "#mm"  "#m##         "mmm"  #      #    " mm#mm  #   ##  "mmm"
                                                                             


Welcome! The game is easy: you jump on a sPRiNG.
How high will you fly?

LEVEL (1/30)

Guess the height: LEVEL (2/30)

Guess the height: LEVEL (3/30)

Guess the height: LEVEL (4/30)

Guess the height: LEVEL (5/30)

Guess the height: LEVEL (6/30)

Guess the height: LEVEL (7/30)

Guess the height: LEVEL (8/30)

Guess the height: LEVEL (9/30)

Guess the height: LEVEL (10/30)

Guess the height: LEVEL (11/30)

Guess the height: LEVEL (12/30)

Guess the height: LEVEL (13/30)

Guess the height: LEVEL (14/30)

Guess the height: LEVEL (15/30)

Guess the height: LEVEL (16/30)

Guess the height: LEVEL (17/30)

Guess the height: LEVEL (18/30)

Guess the height: LEVEL (19/30)

Guess the height: LEVEL (20/30)

Guess the height: LEVEL (21/30)

Guess the height: LEVEL (22/30)

Guess the height: LEVEL (23/30)

Guess the height: LEVEL (24/30)

Guess the height: LEVEL (25/30)

Guess the height: LEVEL (26/30)

Guess the height: LEVEL (27/30)

Guess the height: LEVEL (28/30)

Guess the height: LEVEL (29/30)

Guess the height: LEVEL (30/30)

Guess the height: Congratulation! You've won! Here is your flag:

picoCTF{pseudo_random_number_generator_not_so_random_248ec303}
```