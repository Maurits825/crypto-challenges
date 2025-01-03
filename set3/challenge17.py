import random

from my_crypto import encrypt_cbc, decrypt_cbc
from utils import get_random_bytes, str2bin

string_inputs = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

key = get_random_bytes(16)
iv = get_random_bytes(16)


def encrypt():
    s = string_inputs[random.randint(0, len(string_inputs) - 1)]
    e = encrypt_cbc(str2bin(s), iv, key)
    return e, s


def decrypt(e: bytes):
    try:
        d = decrypt_cbc(e, iv, key)
    except ValueError:
        return False

    return True


def run():
    e_original, target = encrypt()

    key_size = 16
    total_blocks = int(len(e_original) / key_size)
    plain_texts = []
    e = iv + e_original
    for i in range(total_blocks):
        s = i * key_size
        blocks = e[s:s + 2 * key_size]
        plain = decrypt_last_block(blocks, key_size)
        plain_texts.append(plain)

    pad_count = find_padding_count(e[-2 * key_size:], key_size)
    final_text = "".join(plain_texts)[:-pad_count]

    print("Target:", target)
    print("Decrypted:", final_text)
    print("Same:", target == final_text)


def decrypt_last_block(e: bytes, key_size) -> str:
    assert len(e) == 2 * key_size

    plain_text = [[] for _ in range(key_size)]
    indices = [0] * key_size
    pad_count = 1
    while pad_count <= key_size:
        e_tamper = bytearray(e)
        for i in range(pad_count - 1):
            e_tamper[key_size - i - 1] ^= (ord(plain_text[i][indices[i]]) ^ pad_count)

        byte_index = key_size - pad_count
        byte_value = e_tamper[byte_index]
        for i in range(256):
            e_tamper[byte_index] = byte_value ^ i
            is_valid = decrypt(e_tamper)
            if is_valid:
                plain_text[pad_count - 1].append(chr(pad_count ^ i))

        if len(plain_text[pad_count - 1]) == 0:
            index = pad_count - 2
            indices[index] += 1
            while indices[index] >= len(plain_text[index]):
                indices[index] = 0
                plain_text[index] = []
                index -= 1
                indices[index] += 1
                pad_count -= 1
        else:
            pad_count += 1

    final_p = []
    for i, p in enumerate(plain_text):
        final_p.append(p[indices[i]])

    final_p.reverse()
    text = "".join(final_p)
    return text


def find_padding_count(e: bytes, key_size) -> int:
    assert len(e) == 2 * key_size
    for i in range(0, key_size):
        e_tamper = bytearray(e)
        e_tamper[i] ^= 1
        is_valid = decrypt(e_tamper)
        if not is_valid:
            return key_size - i

    return 0


if __name__ == "__main__":
    run()
