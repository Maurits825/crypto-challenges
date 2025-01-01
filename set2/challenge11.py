import math
import random
from enum import Enum

from my_crypto import encrypt_aes_ecb, encrypt_cbc
from utils import get_random_bytes, str2bin


class EncryptMode(Enum):
    ECB = 1
    CBC = 2


def detect_ecb_old(binary):
    byte_frequencies = []
    byte_size_check = [16]
    binary_size = len(binary)
    for byte_size in byte_size_check:
        blocks = math.ceil(binary_size / byte_size)
        cumulative_avg_frequency = 0
        for o in range(0, 16):
            byte_dict = dict()
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

            freqs = [v for v in byte_dict.values()]
            cumulative_avg_frequency += sum(freqs) / len(freqs)
        byte_frequencies.append(cumulative_avg_frequency)
    avg = sum(byte_frequencies) / len(byte_frequencies)
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


# TODO mostly works, depends on the plain text though
def detect_ecb(ciphertext, block_size=16):
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) - len(set(blocks))


def run():
    with open("english_text.txt", 'r') as f:
        text = f.read()
    # text = "YELLOW SUBMARINE"[:] * 100
    for i in range(10):
        encrypted, mode = encryption_oracle(str2bin(text))
        score = detect_ecb(encrypted)
        print(mode, score)


def find_encrypt_ecb():
    with open("../set1/data8.txt", 'r') as file:
        for n, line in enumerate(file):
            binary = bytes.fromhex(line)
            print(n, detect_ecb(binary))


if __name__ == "__main__":
    # find_encrypt_ecb()
    run()
