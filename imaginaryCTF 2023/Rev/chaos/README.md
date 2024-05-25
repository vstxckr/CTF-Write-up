# CHAOS

## Mô tả

- Mô tả challenge.
</br>![img](/imaginaryCTF%202023/Rev/chaos/assets/des.png)

- Bài cho chúng ta một file python chứa source python thực hiện nhận đầu vào là flag và cho ra kết quả là đúng hoặc sai.

- Sau khi format bằng online tool xong thì mình có dược file [formatted.py](/imaginaryCTF%202023/Rev/chaos/chall/formatted.py), trông dễ đọc hơn xíu.

## Ý tưởng

- File source thực chất được deobfuscate bằng cách sử dụng các vòng for để duyệt các attribute, câu lệnh kiểm tra để lấy được attribute mong muốn và sau đó là lấy nó ra và thực hiện nó như hàm hoặc đối tượng.

- Việc deobfuscate bài này cũng không dễ, mình nghĩ là tốn khá nhiều thời gian nên mình đã đi tìm một số cách khác. Và mình để ý được rằng là đoạn mã này có phần kiểm tra khá lộ liễu =)).
</br>![img](/imaginaryCTF%202023/Rev/chaos/assets/check.png)

- nó sẽ lấy phần tử thứ a ^ b (.__getitem__(a ^ b)) sau đó sử dụng hàm pow(x) để mũ phần tử đó lên x lần và kiểm tra với .__eq__(y) xem có bằng hay không, nếu có thì thực hiện kiểm tra tiếp, còn không thì in ra sai.

- Mình sẽ sử dụng nvim để lấy hết những đoạn kiểm tra này và cho vào file [solve.py](/imaginaryCTF%202023/Rev/chaos/chall/solve.py), mình tìm thấy có 51 cái, làm tay cũng không tốn nhiều thời gian.

- Tiếp đó mình sẽ replace một chút trong file solve.py để được format là `t = , r = , n = ` tiếp đến là thêm một chút script vào là được file solve.py hoàn chỉnh.

- Chạy file solve.py và ta có được flag.

## Script

- Script ở đây [solve.py](/imaginaryCTF%202023/Rev/chaos/chall/solve.py).

## Kết quả

![img](/imaginaryCTF%202023/Rev/chaos/assets/res.png)

> Flag: ictf{pYthOn_obFuScAtION_iS_N0_M4TCH_f0r_U_9e1b23f9}
