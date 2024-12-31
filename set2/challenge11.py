import math
import random
from enum import Enum

from my_crypto import encrypt_aes_ecb, encrypt_cbc
from utils import get_random_bytes, str2bin


class EncryptMode(Enum):
    ECB = 1
    CBC = 2


def detect_ecb(binary):
    unique_blocks_percent = []
    byte_size_check = [16]
    for byte_size in byte_size_check:
        blocks = math.ceil(len(binary) / byte_size)
        byte_dict = dict()
        cummulative_percent = 0
        for o in range(0, byte_size):
            for i in range(blocks):
                s = o + (i * byte_size)
                bits = binary[s:s + byte_size]
                bits_hash = 0
                for b in bits:
                    bits_hash |= b
                    bits_hash <<= 8
                if bits_hash in byte_dict:
                    byte_dict[bits_hash] += 1
                else:
                    byte_dict[bits_hash] = 1

            byte_dict_len = len(byte_dict)
            cummulative_percent += byte_dict_len / blocks
        unique_blocks_percent.append(cummulative_percent / byte_size)
    avg = sum(unique_blocks_percent) / len(unique_blocks_percent)
    return avg


def encryption_oracle(b_in: bytes) -> (bytes, EncryptMode):
    pre = get_random_bytes(random.randint(5, 10))
    suf = get_random_bytes(random.randint(5, 10))
    binary = pre + b_in + suf

    key = get_random_bytes(16)
    r = random.randint(1, 2)
    if r == 1:
        encrypted = encrypt_aes_ecb(binary, key)
        mode = EncryptMode.ECB
    else:
        iv = get_random_bytes(16)
        encrypted = encrypt_cbc(binary, iv, key)
        mode = EncryptMode.CBC

    return encrypted, mode


def run():
    with open("english_text.txt", 'r') as f:
        text = f.read()
    # text = "YELLOW SUBMARINE" * 100
    for i in range(10):
        encrypted, mode = encryption_oracle(str2bin(text))
        print(mode, detect_ecb(encrypted))


def find_encrypt_ecb():
    with open("../set1/data8.txt", 'r') as file:
        for n, line in enumerate(file):
            binary = bytes.fromhex(line)
            print(n, detect_ecb(binary))


if __name__ == "__main__":
    # find_encrypt_ecb()
    run()
