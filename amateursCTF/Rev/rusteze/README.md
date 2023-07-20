# RUSTEZE

## Overview

![img](/amateursCTF/Rev/rusteze/assets/overview.png)

- Bài cho chúng ta file `rusteze`, decompile nó ra thì trông như là file thực thi của rust.

## Analyze

- Đây có lẽ là hàm main:
</br>![img](/amateursCTF/Rev/rusteze/assets/main.png)

- Sau khi debug và rà soát một loạt thì có vẻ như chương trình chỉ thực hiện mã hóa một cách đơn giản.

- Chương trình sẽ cho nhập input và kiểm tra xem input có 38 ký tự hay không, nếu có thì nó sẽ set up một mảng bao gồm 38 ký tự như sau. Mình sẽ đặt tên cho mảng `v13` này là `key`.
</br>![img](/amateursCTF/Rev/rusteze/assets/v13.png)

- Tiếp theo nó sẽ chạy thuật toán này để mã hóa input đầu vào.
</br>![img](/amateursCTF/Rev/rusteze/assets/enc.png)

- Thuật toán có thể được viết lại như sau.

```c
for ( int i = 0 ; i < 38 ; i++ )
{
    temp = key[i] ^ input[i]
    rol(temp, 2); // (rotate left 2 bit)
    cipher[i] = temp;
}
```

- Sau đó nó sẽ kiểm tra mảng `char cipher[]`  với mảng sau, do được decompile nên trông nó hơi có vẻ lỗi, nhưng nó là một mảng 38 phần tử char.
</br>![img](/amateursCTF/Rev/rusteze/assets/encrypted.png)

- Như vậy là ta đã có đủ thông tin để lấy lại được message đúng. Việc còn lại chỉ là đảo ngược thuật toán để lấy lại nó.

## Code

```c
#include<stdio.h>

int main()
{
	unsigned char out[] =
	{
	  0x19, 0xEB, 0xD8, 0x56, 0x33, 0x00, 0x50, 0x35, 0x61, 0xDC, 
	  0x96, 0x6F, 0xB5, 0x0D, 0xA4, 0x7A, 0x55, 0xE8, 0xFE, 0x56, 
	  0x97, 0xDE, 0x9D, 0xAF, 0xD4, 0x47, 0xAF, 0xC1, 0xC2, 0x6A, 
	  0x5A, 0xAC, 0xB1, 0xA2, 0x8A, 0x59, 0x52, 0xE2
	};
	unsigned char salt[] =
	{
	  0x27, 0x97, 0x57, 0xE1, 0xA9, 0x75, 0x66, 0x3E, 0x1B, 0x63, 
	  0xE3, 0xA0, 0x05, 0x73, 0x59, 0xFB, 0x0A, 0x43, 0x8F, 0xE0, 
	  0xBA, 0xC0, 0x54, 0x99, 0x06, 0xBF, 0x9F, 0x2F, 0xC4, 0xAA, 
	  0xA6, 0x74, 0x1E, 0xDD, 0x97, 0x22, 0xED, 0xC5
	};	

	for (int i = 0 ; i < 38 ; i++ )
	{
		out[i] = (((out[i] & 0x3) << 6) | (out[i] >> 2));
		printf("%c", out[i]^salt[i]);
	}
}
```

## Result

![img](/amateursCTF/Rev/rusteze/assets/result.png)

>### Flag: amateursCTF{h0pe_y0u_w3r3nt_t00_ru5ty}