# TRICK-QUESTION

## Overview

![img](/amateursCTF/Rev/trick-question/assets/overview.png)

- Bài cho chúng ta một file tên là `trick-question.pyc`, dưới đây là thông tin của file.
</br>![img](/amateursCTF/Rev/trick-question/assets/info.png)

## Decompile

### 1. Lần 1

- Sau khi đọc mô tả challenge thì mình bắt tay vào cài `python 3.10` và đi tìm một số tool để decompile cái file này.
</br>![img](/amateursCTF/Rev/trick-question/assets/run_test.png)

- Mình có tìm được khá nhiều tool hay ho, nhưng mà [pycdc](https://github.com/zrax/pycdc) được recommend nhiều nhất vì nó hỗ trợ python 3.10.

- Chạy thử lệnh để decompile file này. Mình được một file code python đặt tên là `decompiled_1.py`.
</br>![img](/amateursCTF/Rev/trick-question/assets/decm_1.png)

### 2. Lần 2

- Mở nó lên thì trông nó khá bruh nên mình thử chạy nó ra xem như nào. Nhưng nó vẫn ra kết quả như lúc chạy file `trick-question.py`.
</br>![img](/amateursCTF/Rev/trick-question/assets/run_dcm1.png)

- Mình nhận thấy là chả có chỗ nào in ra `Enter the flag:` nhưng khi chạy vẫn in ra, nên mình thử in ra kết quả của `b64decode()` xem có gì.
</br>![img](/amateursCTF/Rev/trick-question/assets/next_run.png)

- Kết quả là một file script khác =)), mình đặt tên nó là `dcm1_run.py`. Mình đã bôi đen đoạn chuỗi, nó hint cho chúng ta sử dụng pycdc để decompile marshaled code object.
</br>![img](/amateursCTF/Rev/trick-question/assets/dcm_1.png)
</br>![img](/amateursCTF/Rev/trick-question/assets/pycdc_usage.png)

- Xem xét file `dcm1_run.py` thì mình thấy đối tượng `code` giống như code được compile ra. Mình thử dùng `print()` để in thì.
</br>![img](/amateursCTF/Rev/trick-question/assets/print_code.png)

- Vậy ra nó là code object. Mình sẽ sử dụng thư viện marshal để dumps toàn bộ code này vào file mới và decompile tiếp bằng pycdc.
</br>![img](/amateursCTF/Rev/trick-question/assets/dong_hom.png)

- Trông cũng hòm hòm rùi, let's đóng hòm time.
- Mình sẽ sử dụng pycdc lần nữa để decompile `dumps.pyc`. `pycdc -v 3.10 -c dumps.pyc -o decompiled_2.py`.
</br>![img](/amateursCTF/Rev/trick-question/assets/dcm_2.png)

## Rewrite Script

- Vứt cho chatgpt code lại và ta được file mới là `code.py`.
</br>![img](/amateursCTF/Rev/trick-question/assets/code.png)

## Tìm flag

- Đoạn đầu sẽ check xem có đúng flag form và message bên trong có dài 42 ký tự không.
</br>![img](/amateursCTF/Rev/trick-question/assets/if_0.png)

- Tiếp theo là check xem các vị trí dấu gạch dưới xem có nằm đúng vị trí không.
</br>![img](/amateursCTF/Rev/trick-question/assets/underscore.png)

- Như vậy độ dài chuỗi message là 42, có 6 vị trí của dấu gạch dưới -> sẽ có 7 phần tiếp theo cần kiểm tra. Mình sẽ đánh số từ 0 đến 6.

### 1. Part 0

- Part 0 chỉ kiểm tra xem đảo ngược của phần tử này có bằng 'sn0h7YP' hay không. Như vậy Part 0 sẽ là 'PY7h0ns'.
</br>![img](/amateursCTF/Rev/trick-question/assets/p0.png)

### 2. Part 1

- Part 1 kiểm tra hệ phương trình 3 ẩn, giải ra được `[97, 114, 51]`
</br>![img](/amateursCTF/Rev/trick-question/assets/p1.png)

### 3. Part 2

- Tới đây chương trình sẽ kiểm tra xem hash sha256 của Part 2 (1 ký tự) có bằng '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'.
</br>![img](/amateursCTF/Rev/trick-question/assets/p2.png)

- Mình sẽ sử dụng phương pháp brute-force để tìm kiếm kí tự này.
</br>![img](/amateursCTF/Rev/trick-question/assets/brute.png)

- Như vậy kí tự cần tìm là '4'.

### 4. Part 3

- Tiếp theo là một đoạn kiểm tra xem shuffle của chuỗi đầu vào (chưa biết) với seed là ký tự vừa tìm (đã biết). Xem có bằng `[49, 89, 102, 109, 108, 52]` hay không.
</br>![img](/amateursCTF/Rev/trick-question/assets/p3.png)

- Cách giải quyết cũng không quá khó, mình sẽ tạo ra tất cả các hoán vị của mảng kiểm tra, sau đó đặt nó làm input cho phương thức `shuffle()` với seed là ký tự '4'
</br>![img](/amateursCTF/Rev/trick-question/assets/p3_d.png)

- Chuỗi cần tìm là 'f4m1lY'.

### 5. Part 4

- Part 4 chỉ kiêm tra đơn giản, kết quả là '0f'.
![img](/amateursCTF/Rev/trick-question/assets/p4.png)

### 6. Part 5

- Part 5 sẽ chuyển chuỗi thành 3 khối 4 bytes sau đó thực hiện xor mỗi khối với một giá trị trả về của hàm `randint(0, 0xffffffff)`.
</br>![img](/amateursCTF/Rev/trick-question/assets/p5.png)

- Trông có vẻ khó nhưng thực ra rất dễ vì mình biết được seed rồi.
</br>![img](/amateursCTF/Rev/trick-question/assets/p5_d.png)

### 7. Part 6

- Part 6 khá đơn giản, việc nó thực hiện chỉ là cộng code ASCII của kí tự vào một biến output sau đó dịch 7 bit sang trái và lặp lại.
</br>![img](/amateursCTF/Rev/trick-question/assets/p6.png)

- Việc decrypt cũng khá đơn giản, chỉ cần làm như bên dưới.
</br>![img](/amateursCTF/Rev/trick-question/assets/p6_d.png)

## Script

```python
import hashlib
import itertools
import random

####################################################################################
# INIT
part = ["", "", "", "", "", "", ""]

####################################################################################
# PART 0
part[0] = 'sn0h7YP'
part[0] = part[0][::-1]
print('part 0 -', part[0])

####################################################################################
# PART 1
part[1] = ''.join(list(map(chr, [97, 114, 51])))
print('part 1 -', part[1])

####################################################################################
# PART 2
for i in range(256):
    value = hashlib.sha256(chr(i).encode()).hexdigest()
    if (value == '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'):
        part[2] = chr(i)
        print('part 2 -', part[2])

####################################################################################
# PART 3
sample = [49, 89, 102, 109, 108, 52]
perm = list(itertools.permutations(sample))
for i in perm:
    random.seed(b'4') 
    temp = list(i)
    random.shuffle(temp)
    if (temp == sample):
        res =  list(map(chr, list(i)))
        part[3] = ''.join(res)
        print('part 3 -', part[3])

####################################################################################
# PART 4
part[4] = "0f"

####################################################################################
# PART 5
sample = [49, 89, 102, 109, 108, 52]
xor_res = [0xFBFF4501, 825199122, 0xFEEF2AA6]
input = [b"", b"", b""]
random.seed(b'4')
random.shuffle(sample)
input[0] = (random.randint(0, 0xFFFFFFFF) ^ xor_res[0]).to_bytes(4, 'little')
input[1] = (random.randint(0, 0xFFFFFFFF) ^ xor_res[1]).to_bytes(4, 'little')
input[2] = (random.randint(0, 0xFFFFFFFF) ^ xor_res[2]).to_bytes(4, 'little')
part[5] = b''.join(input).decode()
print('part 5 -', part[5])

####################################################################################
# PART 6
d = 0x29ee69af2f3
for i in range(6, -1, -1):
    part[6] += chr(d >> 7*i & 0x7f)
print('part 6 -', part[6])

# FLAG 
flag = "amateursCTF{" + '_'.join(part) + "}"
print('flag:', flag)
```

## Result

![img](/amateursCTF/Rev/trick-question/assets/res.png)

>### Flag: amateursCTF{PY7h0ns_ar3_4_f4m1lY_0f_N0Nv3nom0us_Sn4kes}