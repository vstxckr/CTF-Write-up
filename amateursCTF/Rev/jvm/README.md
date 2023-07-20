# JVM

## Overview

![img](/amateursCTF/Rev/jvm/assets/overview.png)

- Bài cho chúng ta 2 file (file code.jvm trong file nén bị sai nên úp riêng). Giải nén file `jvm.tar.gz` ra ta được thư mục gồm 2 file là `code.jvm` và `JVM.class`.

## Decompile JVM.class

- Mình sẽ cho file `JVM.class` chứa Java bytecode vào Java decompiler để trích xuất code của nó ra. Mình sẽ lưu vào file tên là `decompile_src.java`.
</br>![img](/amateursCTF/Rev/jvm/assets/decompile.png)

- Chương trình này sẽ tạo ra file JVM.class để cho chúng ta thực thi. Hàm main của nó sẽ yêu cầu đối số từ dòng lệnh, đối số này là tên file, file sẽ được mở dưới dạng từng phần tử byte trong một mảng static của class JVM. Sau đó nó gọi đến phương thức `vm()` được định nghĩa ngay phía dưới.
</br>![img](/amateursCTF/Rev/jvm/assets/main.png)

- Hàm `vm()` sau một hồi mình xem qua thì nó như là một bảng định nghĩa những instruction đồng thời là một trình thực thi luôn, nó sẽ sử dụng:
    - Biến b làm con đếm chương trình (PC). 
    - b3, b4 sẽ là 2 thanh ghi lưu đối số truyền vào (nếu lệnh đó dùng đến đối số).
    - arrayOfInt2 là mảng gồm 4 thanh ghi, theo mình thấy thì chức năng của nó gần giống kiểu như trong nasm (eax, ebx, ecx, edx).
    - arrayOfInt1 là vùng nhớ cho nhập input.

- Còn đoạn này ko cần quan tâm =)).
</br>![img](/amateursCTF/Rev/jvm/assets/last.png)

- Về source được decompile mình chỉ nói như vậy thôi, nếu muốn hiểu hơn thì hãy đọc kĩ code.

## Disassemble code.jvm

- Bây giờ mình sẽ làm một bước nữa là disassemble cái file `code.jvm` kia, bằng cách là thêm những dòng in ra màn hình trong mỗi instruction, tắt những lệnh in màn và đọc từ bàn phím và cũng tắt chức năng nhảy của những lệnh `jmp`, như vậy thì phương thức `vm()` chỉ đọc bytecode từ `code.jvm` rồi in ra ý nghĩa của instruction đó. À, đồng thời với đó mình cũng sẽ in ra địa chỉ để dễ quan sát.
</br>![img](/amateursCTF/Rev/jvm/assets/code_decom.png)

- Sau một hồi sửa thì mình có được file `code_decom.java`. Compile file này thì mình sẽ được `code_decom.class`, việc còn lại chỉ cần chạy file này là có được toàn bộ code của chương trình dưới dạng mã assembly mình tự nghĩ ra. Chạy `javac code_decom.java` sau đó chạy `java code_decom > disasm.code` ta được file `disasm.code` chứa code được disasemble từ file `code.jvm`, đồng thời mình cũng thay những tến biến cho dễ đọc.
</br>![img](/amateursCTF/Rev/jvm/assets/disasm.png)

- Kiểm tra file code vừa được disassemble, mình thấy ở cuối có đoạn kiểm tra với flag, ở đoạn này mình sẽ dùng nvim lấy chay data nó ra để được file `export.c`. Tuy nhiên có một kí tự sẽ dùng một số thủ thuật để kiểm tra.
</br>![img](/amateursCTF/Rev/jvm/assets/export.png)

- Và thật bất ngờ ta có được gần như toàn bộ flag :kissing:.

- Hiện giờ chỉ có một kí tự chưa tìm thấy, mình quyết định brute-force luôn (mặc dù thực tế lúc mình làm file code bị lỗi nên ko brute được, mình làm chay :skull:).
</br>![img](/amateursCTF/Rev/jvm/assets/yes.png)

- Vậy kí tự còn thiếu là 'A'. Ghép lại ta được flag hoàn chỉnh.

>### Flag: amateursCTF{wh4t_d0_yoU_m34n_j4v4_isnt_A_vm?}