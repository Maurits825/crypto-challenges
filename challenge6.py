import math

from challenge3 import brute_force_key
from utils import *


def decrypt():
    with open("data6.txt", 'r') as file:
        b64 = file.read()

    binary = base64.b64decode(b64)

    key_distance = []
    for key_size in range(2, 40):
        b1 = binary[:key_size]
        b2 = binary[key_size:2 * key_size]
        d = get_hamming_distance(b1, b2) / key_size
        key_distance.append((key_size, d))

    key_distance.sort(key=lambda x: x[1])
    print("best keysizes:", key_distance[:3])

    for key_tuple in key_distance[:3]:
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
            keys.append(k)
        continue


if __name__ == "__main__":
    decrypt()
