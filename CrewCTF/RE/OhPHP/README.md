# OhPHP

![img](/CrewCTF/RE/OhPHP/assets/chall.png)

## MỤC LỤC

- [I. Overview](#i-overview).
- [II. Idea](#ii-idea).
    - [1. Idea 1 - Compile ra file thực thi và dùng IDA decompile](#1-idea-1---compile-ra-file-thực-thi-và-dùng-ida-decompile).
    - [2. Idea 2 - Decrypt lại file chall.php](#2-idea-2---decrypt-lại-file-challphp).
        - [2.1 Rà soát file mã hóa](#21-rà-soát-file-mã-hóa).
        - [2.2 Giải mã tìm source code](#22-giải-mã-tìm-source-code).
            - [2.2.1 Lần 1 - loại bỏ biểu thức trong ngoặc có từ 2 - 4 toán hạng](#221-lần-1---loại-bỏ-biểu-thức-trong-ngoặc-có-từ-2---4-toán-hạng).
            - [2.2.2 Lần 1.5 - thay thế ký tự '0'](#222-lần-15---thay-thế-ký-tự-'0').
            - [2.2.3 Lần 2 - Rà soát những biểu thức có ký tự đặc biệt hoặc có biểu thức có từ 5 toán hạng trở lên](#223-lần-2---rà-soát-những-biểu-thức-có-ký-tự-đặc-biệt-hoặc-có-biểu-thức-có-từ-5-toán-hạng-trở-lên).
            - [2.2.4 Lần 3 - Sử dụng chatgpt để khôi phục lại code ban đầu](#224-lần-3---sử-dụng-chatgpt-để-khôi-phục-lại-code-ban-đầu).
- [III. Tìm Flag](#iii-tìm-flag).
    - [1. Lệnh if thứ 1](#1-lệnh-if-thứ-1).
    - [2. Lệnh if thứ 2](#2-lệnh-if-thứ-2).
    - [3. Lệnh if thứ 3](#3-lệnh-if-thứ-3).
    - [4. Lệnh if thứ 4 và 5](#4-lệnh-if-thứ-4-và-5).
- [IV. Script Solve](#iv-script-solve).
- [V. Kết quả chạy Script](#v-kết-quả-chạy-script).
- [VI. Flag](#vi-flag).

## I. Overview

- Bài cho chúng ta một file tên là [chall.php](/CrewCTF/RE/OhPHP/chall/chall.php). File này là có đuôi `.php` nên mình nghĩ là code PHP.
- Tuy nhiên bên trong nó khá tởm, dài loằng ngoằng và có vẻ như đã được mã hóa bằng một cách nào đó mà mình chưa biết (bởi vì mình chưa thực sự code `php` bao giờ :confused:)

![img](/CrewCTF/RE/OhPHP/assets/chall_content.png)

- Mình có để ý là ở cuối file cũng thiếu cặp ngoặc đóng `?>` nên mình đã thêm vào sau đó.

- Việc đầu tiên mình làm là thử chạy file này xem nó làm những gì.

![img](/CrewCTF/RE/OhPHP/assets/run_test.png)

- Như vậy là chương trình sẽ in ra một banner trông khá cute và cho hiện dòng thông báo người dùng nhập `Flag`. 
- Tuy nhiên chúng ta vẫn chưa biết được rằng ở file code chứa những gì nên mình đã có một số ý tưởng..

## II. IDEA

- Với bài này thì ban đầu mình nghĩ rằng bên trong file `.php` kia cũng sẽ có những dòng code như bình thường, in ra màn hình, cho phép nhập input, kiểm tra input và đưa ra kết quả. 
- Điều đó có nghĩa là nếu ta biết được những dòng code bên trong nó làm những gì thì ta sẽ có thể lấy được bí mật bên trong nó (flag).
- Do giới hạn về thời gian và file được mã hóa trông khá cồng kềnh, nên mình chỉ nghĩ được 2 ý tưởng bên dưới đây.

### 1. Idea 1 - Compile ra file thực thi và dùng IDA decompile

- Sau một hồi tìm hiểu trên internet mình có tìm được một số công cụ tên là `ExeOutput for PHP` để compile file code `chall.php` ra được file thực thi `.exe` của Windows.

![img](/CrewCTF/RE/OhPHP/assets/compile.png)

- Phần mềm này sử dụng trên Windows khá dễ dàng và có giao diện khá trực quan.
- Sau một hồi mày mò thì mình cũng tìm được cách để compile file code `chall.php` ra [chall_output.exe](/CrewCTF/RE/OhPHP/chall/chall_output.exe).

- File chạy bình thường trên máy mình, nên tiếp theo đó là mình decompile bằng IDA luôn.

![img](/CrewCTF/RE/OhPHP/assets/ida_re.png)

- Tuy nhiên sau một hồi mày mò thì mình thấy rằng nó cũng khó đọc không kém và sau đó mình đã chuyển sang ý tưởng thứ 2.

### 2. Idea 2 - Decrypt lại file chall.php

#### 2.1 Rà soát file mã hóa

- Do quá bất lực với file vừa compile được nên mình đã chuyển hướng sang phân tích xem file `chall.php` có gì hay.
- Lúc đầu mình thử cho một phần đống code này lên đủ loại tool trên mạng tìm kiếm nhưng đều không có được kết quả gì. Nên sau đó mình đã ngồi lại và thử bóc tách từng đoạn code ra chạy xem nó cho ra kết quả như nào.

![img](/CrewCTF/RE/OhPHP/assets/char.png)

- Như vậy là những phân tử nhỏ này sẽ tạo ra từng ký tự bằng phép ``xor` - ^` 2 ký tự khác với nhau. Tiếp đó nó dùng phép `nối chuỗi - .` trong `PHP` và được như sau.

![img](/CrewCTF/RE/OhPHP/assets/concat_string.png)

#### 2.2 Giải mã tìm source code

##### 2.2.1 Lần 1 - loại bỏ biểu thức trong ngoặc có từ 2 - 4 toán hạng

- Theo quan sát của mình thì trong file gốc tác giả sử dụng khoảng 8 ký tự là (`'['`, `']'`, `'('`, `')'`, `':'`, `','`, `'.'`, `'?'`).

- Do đó mình viết một file code [gen_char_1.php](/CrewCTF/RE/OhPHP/decrypt_php/reduce_1/gen_char_1.php) đơn giản để thực hiện phép toán ``xor`` cho chỉnh hợp lặp của tập hợp này, nó sẽ in ra những bộ có thể cho ra ký tự có thể in được (trong khoảng từ `32` đến `126`) dưới dạng code python.

![img](/CrewCTF/RE/OhPHP/assets/gen_char.png)

- Sau đó mình copy kết quả vừa nhận được vào một file [replace_1.python](/CrewCTF/RE/OhPHP/decrypt_php/reduce_1/replace_1.py) xem có kết quả như nào.

![img](/CrewCTF/RE/OhPHP/assets/run_replace.png)

- Kết quả ta được file [chall_1_after_run.php](/CrewCTF/RE/OhPHP/decrypt_php/reduce_1/chall_1_after_run.php) mới.

![img](/CrewCTF/RE/OhPHP/assets/replace_1.png)

##### 2.2.2 Lần 1.5 - thay thế ký tự '0'

- Nhận thấy file có một đoạn bị lặp rất nhiều là `''.('a'.'b'.'s')(('s'.'t'.'r'.'s'.'t'.'r')('','.'))` nên mình đã chạy thử và được kết quả là ký tự `'0'`.

![img](/CrewCTF/RE/OhPHP/assets/test.png)

- Sử dụng notepad để replace tất cả những chuỗi bên trên thành `'0'` ta được file [chall_2.php](/CrewCTF/RE/OhPHP/decrypt_php/reduce_2/chall_2.php) mới.

![img](/CrewCTF/RE/OhPHP/assets/notepad_replace.png)

- Ta sẽ thêm ký tự `'0'` vào bảng chữ cái của mảng trong file [gen_char_2.php](/CrewCTF/RE/OhPHP/decrypt_php/reduce_2/gen_char_2.php) và lặp lại các bước bên trên (kết quả chạy được ta sẽ có được [replace_2.py](/CrewCTF/RE/OhPHP/decrypt_php/reduce_2/replace_2.py)) là có thể tối giản gần hết rồi!.

- Sau Khi chạy xong thì ta sẽ được kết quả là file [chall_2_after_run.php](/CrewCTF/RE/OhPHP/decrypt_php/reduce_2/chall_2_after_run.php)

![img](/CrewCTF/RE/OhPHP/assets/replace_2.png)


##### 2.2.3 Lần 2 - Rà soát những biểu thức có ký tự đặc biệt hoặc có biểu thức có từ 5 toán hạng trở lên

- Bây giờ chỉ những biểu thức trong ngoặc đơn có `5` toán hạng trở lên và những ký tự nằm ngoài vùng in được được ra sẽ còn sót lại. Mình rà soát lại thì thấy còn những ký tự dưới đây còn sót.

![img](/CrewCTF/RE/OhPHP/assets/remain_replace.png)

- Replace lại và loại bỏ toán tử nối bằng notepad, ta được kết quả là file [not_formatted.php](/CrewCTF/RE/OhPHP/decrypt_php/not_formatted.php).

![img](/CrewCTF/RE/OhPHP/assets/final_replace.png)

##### 2.2.4 Lần 3 - Sử dụng chatgpt để khôi phục lại code ban đầu

- Sau một loạt những thao tác bên trên thì file hiện tại gần như đã là code rồi nhưng trông vẫn còn khá rối, mình nhờ anh Phong cho vào chatgpt tối giản code lại và được file [formatted](/CrewCTF/RE/OhPHP/decrypt_php/formatted.php).

![img](/CrewCTF/RE/OhPHP/assets/chatgpt.png)


## III. Tìm Flag

### 1. Lệnh if thứ 1

- Như vậy là mình đã hoàn thành xong phần giải mã code để được source ban đầu. Việc còn lại hiện giờ chỉ cần tìm giá trị đúng cho chuỗi cần nhập là xong.
- Dưới đây là những câu lệnh kiểm tra cần phải vượt qua.

![img](/CrewCTF/RE/OhPHP/assets/task.png)

- Ở lệnh `if` đầu tiên sẽ kiểm tra xem `5` ký tự đầu của input có phải là `crew{` hay không. Như vậy là mình đã biết `5` ký tự đầu là `crew{`.

```php
if (in_array(substr(constant("F"), 0, 5), ["crew{"]))
```

### 2. Lệnh if thứ 2

- Câu lệnh `if` tiếp theo sẽ kiểm tra đảo ngược của kết quả thuật toán `crc32` của 4 ký tự tiếp theo có phải là `7607349263` hay không?

```php
if (strstr(strrev(crc32(substr(constant("F"), 5, 4))), "7607349263"))
```

- Với lệnh này thì đơn giản nhất là mình đi kiếm tool trên mạng, và mình đã kiếm ra được một tool sử dụng `python` nhưng bên trong xử lí bằng `C++` để tìm ra input cho đoạn hash hợp lệ. Link tool: [https://github.com/kmyk/zip-crc-cracker](https://github.com/kmyk/zip-crc-cracker).

- Tool này dùng cho file zip nhưng không sao, mình sẽ hardcode cho đoạn input của code `C++` và mình chỉ cần input cho file zip bất kì là xong. Tool sau khi chỉnh sửa ở [đây](/CrewCTF/RE/OhPHP/break_crc32/break.py).

![img](/CrewCTF/RE/OhPHP/assets/hardcode.png)

![img](/CrewCTF/RE/OhPHP/assets/break_crc32.png)

- Như vậy là `4` ký tự tiếp theo từ chỉ số `5` của chuỗi là `php_`

### 3. Lệnh if thứ 3

- Câu lệnh `if` tiếp theo sẽ kiểm tra `4` ký tự vừa tìm được (từ chỉ số `5`) `php_` sử dụng phép toán `xor` với `4` kí tự tiếp theo (từ chỉ số `9`) có ra kết quả là chuỗi `"A\x1b/k"` hay không.

```php
if (strnatcmp("A\x1b/k", substr(constant("F"), 5, 4) ^ substr(constant("F"), 9, 4)))
```

- Với lệnh này thì việc tìm lại khá đơn giản, mình chỉ cần sử dụng phép toán `xor` lại chuỗi mình vừa tìm được là `php_` với chuỗi `"A\x1b/k"` là được chuỗi cần tìm.

![img](/CrewCTF/RE/OhPHP/assets/xor.png)

- `4` ký tự từ vị trí thứ `9` sẽ là `1s_4`.


### 4. Lệnh if thứ 4 và 5

- Tới đây ta sẽ xem xét cả 2 cái `if` cuối.

```php
srand(31337);
define("D", openssl_decrypt("wCX3NcMho0BZO0SxG2kHxA==", "aes-128-cbc", substr(constant("F"), 0, 16), 2, pack("L*", rand(), rand(), rand(), rand())));

if (in_array(array_sum([(ctype_print(constant("D"))), strpos(substr(constant("F"), 15, 17), constant("D"))]), [2]))
```

- Hàm decrypt thực hiện như mô tả trong ảnh sau.

![img](/CrewCTF/RE/OhPHP/assets/openssl_decrypt.png)

- Về cơ bản là nó sẽ sử dụng `2` chuỗi cố định là `$data`, và `$iv` cùng với `16` ký tự đầu tiên của `input` để cho ra output là kết quả được dercypt, sau đó so sánh với `17` ký tự tiếp theo xem nó có giống hay không. Nếu có thì ta đã tìm được `3` ký tự đúng.

- Vậy tức là khi tìm được `3` ký tự đúng rồi thì ta cũng đã tìm được `17` ký tự tiếp theo từ vị trí `15`.

- Câu lệnh `if` tiếp theo sẽ chỉ đơn giản là kiểm tra xem kết quả `base64` của phép toán `xor` `8` ký tự cuối cùng với `hash` `sha256` của `32` ký tự đầu tiên từ input có bằng `BwdRVwUHBQVF` hay không.

```php
if (strcmp(base64_encode(hash("sha256", substr(constant("F"), 0, 32)) ^ substr(constant("F"), 32)), "BwdRVwUHBQVF"))
```

- Với dữ kiện bên trên thì việc tính được `8` ký tự cuối là khả thi, ta sẽ sử dụng đoạn code sau.

```php
<?php
    $str_1 = 32 ký tự đầu tiên;
    $result = base64_decode("BwdRVwUHBQVF") ^ hash("sha256", $str_1);
    echo $result;
?>
```

- Ta có thể thấy, nếu tìm được `3` ký tự tiếp theo từ vị trí thứ `13`, thì có nghĩa là ta sẽ tìm được toàn bộ flag. Mà `3` ký tự này theo kế hoạch của chúng ta sẽ phải brute-force. Chúng ta sẽ bắt đầu thực hiện từng bước theo như dưới đây.

- Mình đầu tiên sẽ tối giản hết những đoạn code có thể để cho code chạy nhanh nhất.

- Đoạn đầu do `seed` của `srand(seed)` là cố định bằng `31337` nên ta có thể sử dụng một đoạn code nho nhỏ để biết được phần chuỗi kết quả sau khi đi qua hàm `pack()`.

![img](/CrewCTF/RE/OhPHP/assets/pack.png)

- Như vậy đoạn `define()` có thể được tối giản như sau.

```php
$str = 16 ký tự đầu của input;
define("D", openssl_decrypt("wCX3NcMho0BZO0SxG2kHxA==", "aes-128-cbc", $str, 2, "\x5b\xa6\x65\x5c\x0f\x8d\xbd\x67\x0b\x55\xb4\x7b\x7e\xce\xba\x29"));
```

## IV. Script Solve

- Bước tiếp theo là viết lại phần code để bute-force ra `3` ký tự, nếu tìm được `3` ký tự đúng thì mình sẽ hợp nhất `3` ký tự đó cùng với `17` ký tự tiếp theo vào `16` ký tự đầu, tiếp đó là mình sẽ sử dụng `32` ký tự vừa tìm được để tìm `8` ký tự cuối. Code bên dưới được đặt ở [đây](/CrewCTF/RE/OhPHP/solve/solve.php).

![img](/CrewCTF/RE/OhPHP/assets/solve.png)

## V. Kết quả chạy Script

![img](/CrewCTF/RE/OhPHP/assets/flag.png)

## VI. Flag

> Flag: `crew{php_1s_4_l4ngu4ge_0f_m4g1c_5b0e7b6a}`