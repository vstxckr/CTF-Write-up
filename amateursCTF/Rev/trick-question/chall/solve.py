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
