import itertools
import math

from challenge3 import brute_force_key
from challenge5 import repeating_xor_encrypt
from utils import *


def decrypt():
    with open("data6.txt", 'r') as file:
        b64 = file.read()

    binary = base64.b64decode(b64)
    text = bin2str(binary)

    key_distance = []
    for key_size in range(2, 40):
        total_d = 0
        blocks_to_d = 4
        for i in range(blocks_to_d):
            s1 = i * 2 * key_size
            b1 = binary[s1:s1 + key_size]
            b2 = binary[s1 + key_size:s1 + 2 * key_size]
            d = get_hamming_distance(b1, b2) / key_size
            total_d += d
        avg_d = total_d / blocks_to_d
        key_distance.append((key_size, avg_d))

    key_distance.sort(key=lambda x: x[1])
    print("best keysizes:", key_distance[:4])

    for key_tuple in key_distance[:4]:
        key_size = key_tuple[0]
        print("Trying keysize:", key_size)
        binary_blocks = []
        total_blocks = math.ceil(len(binary) / key_size)
        for i in range(total_blocks):
            b = binary[i * key_size:(i + 1) * key_size]
            binary_blocks.append(b)

        transpose_blocks = [[] for _ in range(key_size)]
        for block in binary_blocks:
            for i, b in enumerate(block):
                transpose_blocks[i].append(b)

        keys = []
        for block in transpose_blocks:
            k = brute_force_key(block)
            keys.append(k[:2])

        combinations = itertools.product(range(1, 2), repeat=key_size)
        for c in combinations:
            key = "".join([keys[i][c[i] - 1][0] for i in range(key_size)])
            d = repeating_xor_encrypt(text, key)
            print("Key:", key, "Decrypt partial:", "".join(d[:20]))


def decrypt_w_key():
    with open("data6.txt", 'r') as file:
        b64 = file.read()
    binary = base64.b64decode(b64)
    text = bin2str(binary)
    key = "Terminator X: Bring the noise"
    msg = repeating_xor_encrypt(text, key)
    print("".join(msg))


if __name__ == "__main__":
    # decrypt()
    decrypt_w_key()
