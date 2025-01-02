import random

from my_crypto import encrypt_aes_ecb, detect_ecb
from utils import get_random_bytes, str2bin, base642bin

prefix_bin = get_random_bytes(random.randint(1, 50))
suffix_bin = base642bin(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


def encryption_oracle(b_in: bytes, key: bytes) -> bytes:
    # binary = prefix_bin + b_in + suffix_bin
    binary = b_in + suffix_bin

    encrypted = encrypt_aes_ecb(binary, key)

    return encrypted


def find_key_size(key):
    # start4: smallest key size=2, so 2*2=4 to have two b2b
    smallest_key_size = 4
    for input_size in range(smallest_key_size * 2, 100):
        binary = bytes([ord("A") for _ in range(input_size)])
        encrypt = encryption_oracle(binary, key)

        # key size is prob not 1, otherwise too much chance of b2b bytes
        for key_size in range(smallest_key_size, int(input_size / 2) + 1):
            last_block = None
            blocks = [encrypt[i:i + key_size] for i in range(0, len(encrypt), key_size)]
            for block in blocks:
                if last_block == block:
                    return key_size, (input_size - (2 * key_size))
                last_block = block
    return 0, 0


MAX_ASCII = 128


# theres a chance that a char matches and you get partial garbage outputs
# if we know/assume the plaintext just has 8bit ascii then it should mostly work
# TODO padding at the end?
def find_all_bytes(key_size, key, unknown_byte_size_in, offset):
    unknown_byte_index = unknown_byte_size_in + (key_size - (unknown_byte_size_in % key_size))
    unknown_byte_size = offset + unknown_byte_index
    byte_padding = "A"

    matches = [[] for _ in range(unknown_byte_size)]
    matches_index = [0] * unknown_byte_size
    b = 1
    while b <= unknown_byte_size:
        print("Byte:", b, "/", unknown_byte_size)
        print("".join([chr(matches[i][matches_index[i]]) for i in range(b - 1)]))
        working_block = bytearray([ord(byte_padding) for _ in range(unknown_byte_size)])
        for i in range(b - 1):
            working_block[unknown_byte_size - b + i] = matches[i][matches_index[i]]
        d = encryption_oracle(bytes(working_block[:-b]), key)
        byte_to_find = d[unknown_byte_size - 1]

        for i in range(0, MAX_ASCII):
            c = (i + 32) % MAX_ASCII  # prio control codes last
            working_block[-1] = c
            d = encryption_oracle(bytes(working_block), key)
            if d[unknown_byte_size - 1] == byte_to_find:
                matches[b - 1].append(c)

        if len(matches[b - 1]) == 0:
            index = b - 2
            matches_index[index] += 1
            while matches_index[index] >= len(matches[index]):
                matches_index[index] = 0
                matches[index] = []
                index -= 1
                matches_index[index] += 1
                b -= 1
        else:
            b += 1

    return "".join([chr(matches[i][matches_index[i]]) for i in range(unknown_byte_size)])


def run():
    # key = get_random_bytes(16)
    key = str2bin("YELLOW SUBMARINE")
    # find keysize
    key_size, offset = find_key_size(key)
    print("key size & offset:", key_size, offset)

    # detect ecb...
    text = "YELLOW SUBMARINE" * 100
    encrypted = encryption_oracle(str2bin(text), key)
    score = detect_ecb(encrypted)
    print("is ecb:", score, score > 1)

    t = find_all_bytes(key_size, key, len(suffix_bin), offset)
    print("decrypted:", t)


if __name__ == "__main__":
    run()
