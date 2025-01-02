from my_crypto import encrypt_aes_ecb, detect_ecb
from utils import base642bin, get_random_bytes, str2bin

suffix_bin = base642bin(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")


def encryption_oracle(b_in: bytes, key: bytes) -> bytes:
    binary = b_in + suffix_bin

    encrypted = encrypt_aes_ecb(binary, key)

    return encrypted


def find_key_size(key):
    last_block = None
    for key_size in range(1, 40):
        binary = bytes([ord("A") for _ in range(key_size)])
        encrypt = encryption_oracle(binary, key)
        current_block = encrypt[:key_size]
        if last_block == current_block[:-1]:
            return key_size - 1
        last_block = current_block

    return 0


MAX_ASCII = 128


# theres a chance that a char matches and you get partial garbage outputs
# if we know/assume the plaintext just has 8bit ascii then it should mostly work
# TODO what about the second block of bytes?
def find_first_byte(key_size, key):
    byte_padding = "A"

    matches = [[] for _ in range(key_size)]
    matches_index = [0] * key_size
    b = 1
    while b <= key_size:
        first_block = bytearray([ord(byte_padding) for _ in range(key_size)])
        for i in range(b - 1):
            first_block[key_size - b + i] = matches[i][matches_index[i]]
        d = encryption_oracle(bytes(first_block[:-b]), key)
        byte_to_find = d[key_size - 1]

        for i in range(0, MAX_ASCII):
            c = (i + 32) % MAX_ASCII  # prio control codes last
            first_block[-1] = c
            d = encryption_oracle(bytes(first_block), key)
            if d[key_size - 1] == byte_to_find:
                matches[b - 1].append(c)

        # print("---".join([chr(m) for m in matches[b - 1]]))
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

    return "".join([chr(matches[i][matches_index[i]]) for i in range(key_size)])


def run():
    key = get_random_bytes(16)
    # find keysize
    key_size = find_key_size(key)
    print("key size:", key_size)

    # detect ecb...
    text = "YELLOW SUBMARINE" * 100
    encrypted = encryption_oracle(str2bin(text), key)
    score = detect_ecb(encrypted)
    print("is ecb:", score, score > 1)

    t = find_first_byte(key_size, key)
    print("decrypted first byte:", t)


if __name__ == "__main__":
    run()
