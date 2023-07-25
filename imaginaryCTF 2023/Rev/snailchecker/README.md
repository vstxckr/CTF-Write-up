# SNAILCHECKER

## Mô tả

- Mô tả challenge.
</br>![img](/imaginaryCTF%202023/Rev/snailchecker/assets/des.png)

- Bài cho chúng ta một file tên là check.py chứa source python.

- Chương trình sẽ thực hiện nhận input từ bàn phím, sau đó cắt input đó ra thành những chuỗi gồm 4 ký tự, những chuỗi này sẽ được chứa trong một list.

- Tiếp đó, chương trình sẽ thực hiện một thuật toán mã hóa, đầu tiên từng chuỗi 4 ký tự này sẽ được đảo ngược, sau đó lần lượt chúng sẽ được cho vào hàm enc, giá trị trả về sẽ được chuyển về chuỗi hex và loại bỏ tiền tố '0x', tiếp đến chuỗi đó sẽ được padding '0' vào phía tay trái cho đủ 8 ký tự và được chuyển về chuỗi bytes. Sau cùng là được nối vào biến out. 

- Sau khi thực hiện thuật toán mã hóa, chuỗi out sẽ được kiểm tra với chuỗi `b'L\xe8\xc6\xd2f\xde\xd4\xf6j\xd0\xe0\xcad\xe0\xbe\xe6J\xd8\xc4\xde`\xe6\xbe\xda>\xc8\xca\xca^\xde\xde\xc4^\xde\xde\xdez\xe8\xe6\xde'` xem 2 chuỗi có bằng nhau hay không, nếu có thì in ra Flag correct, ngược lại thì Flag incorrect.

- Mình có xem qua hàm enc và mình biết được hàm này thực chất sử dụng solution của josephus problem nhưng bị deobfuscate nên nó chạy rất rất rất chậm.

## Ý tưởng

- Mình nhận thấy chương trình nhận chuỗi đầu vào và cắt nó ra từng đoạn nhỏ sau đó cho cùng vào một thuật toán mã hóa, tuy nhiên thuật toán mã hóa này chạy rất chậm.

- Vậy thì nếu mình cải tiến thuật toán nó khiến nó chạy rất nhanh và sau đó brute-force nó ra thì sao?

- Nghĩ là làm, mình đã bắt đầu đi tìm hiểu về josephus problem và biết được solution trong bài áp dụng cho trường hợp k = 2 và n < 2^32, mình cũng tìm được solution khác sử dụng bitwise cho trường hợp này từ [wikipedia](https://en.wikipedia.org/wiki/Josephus_problem) độ phức tạp chỉ là O(1).

- Vậy là vấn đề thuật toán mã hóa đã được giải quyết. Giờ mình chỉ cần viết code brute-force là xong.

## Code

- Lưu file và chạy đoạn shell script sau là ta có kết quả: `javac solve.java && java josephus`.

```java
// filename: solve.java
import java.lang.*;
 
class josephus {
 
	public int solve(int n) {
		return ~Integer.highestOneBit(n*2) & ((n<<1) | 1);
	}
	public int brute(int n)
	{
		int x = 0;
		josephus t = new josephus();
		for ( char i = 32 ; i <= 126 ; i++ )
		{
			x = (x & 0xffffff00) | (i); 
			for ( char j = 32 ; j <= 126 ; j++ )
			{
				x = (x & 0xffff00ff) | (j << 8); 
				for ( char k = 32 ; k <= 126 ; k++ )
				{
					x = (x & 0xff00ffff) | (k << 8*2); 
					for ( char l = 32 ; l <= 126 ; l++ )
					{
						x = (x & 0x00ffffff) | (l << 8*3); 
						if (t.solve(x)-1 == n)
						{
							System.out.printf("%x ", x);
						}
					}
				}
			}
		}
		return 0;
	}
    public static void main(String[] args)
    {
		josephus t = new josephus();
        // break from bytes string compare with out in chall.py
		int[] a = {0x4ce8c6d2, 0x66ded4f6, 0x6ad0e0ca, 0x64e0bee6, 0x4ad8c4de, 0x60e6beda, 0x3ec8caca, 0x5ededec4, 0x5ededede, 0x7ae8e6de};

		for ( int i = 0 ; i < 10 ; i++ )
		{
			System.out.printf("turn %d: ", i);
			t.brute(a[i]);
			System.out.print("\n");
		}
    }
}
```

## Kết quả

- Khi chạy xong ta sẽ được những cụm hex từ chuỗi flag.
</br>![img](/imaginaryCTF%202023/Rev/snailchecker/assets/res.png)

- Tuy nhiên ở turn 6 sẽ có 2 nghiệm cho ra cùng một output. Ta sẽ lấy output thứ 2.

- Gom những chuỗi này và cho vào [kt.gy](kt.gy) ta được:
</br>![img](/imaginaryCTF%202023/Rev/snailchecker/assets/decode.png)

- Sau đó chạy đoạn script python nho nhỏ này là ta đã có flag.

```python
def get_flag(s):
     t = ''.join([s[i:i+4][::-1] for i in range(0, len(s), 4)])
     print(t)
s = "ftcisoj{uhperp_selbops_m_deeoooboooo}tso"
get_flag(s)
```

</br>![img](/imaginaryCTF%202023/Rev/snailchecker/assets/decode.png)

> Flag: ictf{josephus_problem_speed_boooooooost}

