# SIX FIVE O TWO

> Cate: Hardware

# Description

Challenge cho chúng ta IP và Port tới một server thực hiện công việc như của một chiếc máy tính tối giản, gồm có RAM, CPU là 6052 với tập lệnh và có 2 ROM, ROM1 chứa flag, và ROM2 là nơi ta có thể flash lệnh vào để cho 6052 thực thi.

![img](/HTB2024/hardware_six-five-o-two/Image/description.png)

Mỗi thành phần đều có không gian địa chỉ riêng.

# Capture The Flag

Để có thể lấy được flag, ta sẽ cần phải thực hiện flash ROM2 với đoạn lệnh dịch chuyển đống flag trong ROM1 ra CONSOLE.

Việc tìm hiểu lệnh cũng không mất quá nhiều thời gian khi mà 6502 khá phổ biến [instruction set](https://www.masswerk.at/6502/6502_instruction_set.html#LDA), [emulator](https://skilldrick.github.io/easy6502/)

Đoạn code cần thiết không quá phức tạp, chỉ là thêm từng byte từ ROM1 vào thanh ghi A rồi lại ghi giá trị thanh ghi A vào CONSOLE tại vị trí tương ứng.

```
LDA $4000
STA $6000
LDA $4001
STA $6001
LDA $4002
STA $6002
LDA $4003
STA $6003
LDA $4004
STA $6004
LDA $4005
STA $6005
LDA $4006
STA $6006
LDA $4007
STA $6007
LDA $4008
STA $6008
LDA $4009
STA $6009
LDA $400A
STA $600A
LDA $400B
STA $600B
LDA $400C
STA $600C
LDA $400D
STA $600D
LDA $400E
STA $600E
LDA $400F
STA $600F
LDA $4010
STA $6010
LDA $4011
STA $6011
LDA $4012
STA $6012
LDA $4013
STA $6013
LDA $4014
STA $6014
LDA $4015
STA $6015
LDA $4016
STA $6016
LDA $4017
STA $6017
LDA $4018
STA $6018
LDA $401A
STA $601A
LDA $401B
STA $601B
LDA $401C
STA $601C
LDA $401D
STA $601D
LDA $401E
STA $601E
LDA $401F
STA $601F
```

Chuyển qua Opcode.

![img](/HTB2024/hardware_six-five-o-two/Image/hexdump_opcode.png)

Lưu ý: 6502 trong bài này thực hiện lấy địa chỉ entry cho việc thực thi ở 2 bytes trước vị trí cuối 2 bytes.

```python
from pwn import *

p = remote ("94.237.60.73","43720")

code = b"AD00408D0060AD01408D0160AD02408D0260AD03408D0360AD04408D0460AD05408D0560AD06408D0660AD07408D0760AD08408D0860AD09408D0960AD0A408D0A60AD0B408D0B60AD0C408D0C60AD0D408D0D60AD0E408D0E60AD0F408D0F60AD10408D1060AD11408D1160AD12408D1260AD13408D1360AD14408D1460AD15408D1560AD16408D1660AD17408D1760AD18408D1860AD19408D1960AD1A408D1A60AD1B408D1B60AD1C408D1C60AD1D408D1D60AD1E408D1E60AD1F408D1F60"
jump = b"0080FFFF"

p.sendline(b"FLASH " + code + b"00"*(0x8000- len(jump)//2 - len(code)//2)+jump )

p.sendline("RUN 65")

p.sendline(b"CONSOLE")

p.interactive()
```