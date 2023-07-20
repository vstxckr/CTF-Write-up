import hashlib
import random

def validate_flag(flag):
    if not flag.startswith('amateursCTF{') or flag[-1] != '}':
        return False

    flag = flag[12:-1]
    if len(flag) != 42:
        return False

    underscores = []
    for i, char in enumerate(flag):
        if char == '_':
            underscores.append(i)
    if underscores != [7, 11, 13, 20, 23, 35]:
        return False

    parts = flag.encode().split(b'_')
    if parts[0][::-1] != b'sn0h7YP':
        return False

    values = [
        int(parts[1][0]) + int(parts[1][1]) - int(parts[1][2]),
        int(parts[1][1]) + int(parts[1][2]) - int(parts[1][0]),
        int(parts[1][2]) + int(parts[1][0]) - int(parts[1][1])
    ]
    if tuple(values) != (160, 68, 34):
        return False

    hash_value = hashlib.sha256(parts[2]).hexdigest()
    if hash_value != '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a':
        return False

    random.seed(parts[2])
    shuffled_list = list(parts[3])
    random.shuffle(shuffled_list)
    if shuffled_list != [49, 89, 102, 109, 108, 52]:
        return False

    if parts[4] + b'freebie' != b'0ffreebie':
        return False

    xor_results = [
        int.from_bytes(parts[5][0:4], 'little') ^ random.randint(0, 0xFFFFFFFF),
        int.from_bytes(parts[5][4:8], 'little') ^ random.randint(0, 0xFFFFFFFF),
        int.from_bytes(parts[5][8:12] + b'\x00', 'little') ^ random.randint(0, 0xFFFFFFFF)
    ]
    if xor_results != [0xFBFF4501, 825199122, 0xFEEF2AA6]:
        return False

    c = 0
    for i in parts[6]:
        c = c * 128 + i
    if hex(c) != '0x29ee69af2f3':
        return False

    return True
