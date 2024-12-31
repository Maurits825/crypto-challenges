import itertools
import math

from challenge7 import decrypt_aes_ecb
from is_english import is_english


def find_encrypt_ecb():
    with open("data8.txt", 'r') as file:
        max_bit_len = 17
        dict_len = [[] for _ in range(1, max_bit_len)]
        for n, line in enumerate(file):
            binary = bytes.fromhex(line)
            for bit_len in range(1, max_bit_len):
                byte_dict = dict()
                blocks = math.ceil(len(binary) / bit_len)
                for i in range(blocks):
                    bits = binary[i * bit_len:(i + 1) * bit_len]
                    bits_hash = 0
                    for b in bits:
                        bits_hash |= b
                        bits_hash <<= max_bit_len
                    if bits_hash in byte_dict:
                        byte_dict[bits_hash] += 1
                    else:
                        byte_dict[bits_hash] = 1
                l = len(byte_dict)
                dict_len[bit_len - 1].append((n, l))

        sort_key = lambda x: x[1]
        for i, d in enumerate(dict_len):
            d.sort(key=sort_key)
            print("Bit Length:", i + 1)
            print("Min:", min(d, key=sort_key), "Max:", max(d, key=sort_key))
            print("Bit pattern lengths (n,l):", d[:20])


def brute_force_key(encrypted):
    combinations = itertools.product(range(0, 100), repeat=16)
    key = bytearray(16)
    for j, c in enumerate(combinations):
        if j % 100000 == 0:
            print("Iteration: ", j)

        for i, v in enumerate(c):
            key[i] = v

        d_bin = decrypt_aes_ecb(encrypted, bytes(key))
        d_char = [chr(d) for d in d_bin]
        score = is_english(d_char)
        if score < 6000:
            print(key)
            print("".join(d_char)[:20])
            print(score)


if __name__ == "__main__":
    find_encrypt_ecb()
    # hex_str = "d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a"
    # brute_force_key(bytes.fromhex(hex_str))
