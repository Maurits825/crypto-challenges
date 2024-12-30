# from https://cryptopals.com/sets/1/challenges/3
from utils import string_xor_key

hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def brute_force_key(h_str: str):
    b = bytes.fromhex(h_str)
    encrypted = [chr(i) for i in b]
    potential_key = []
    for i in range(1000):
        d = string_xor_key(encrypted, chr(i))
        if is_english(d):
            potential_key.append([chr(i), "".join(d)])
    return potential_key


alphabet = 'abcdefghijklmnopqrstuvxyz '


def is_english(chars) -> bool:
    total_chars = len(chars)
    letter_count = 0
    letters = dict()
    for c in chars:
        c_lower = c.lower()
        if c_lower in alphabet:
            letter_count += 1
            if c_lower not in letters:
                letters[c_lower] = 0
            else:
                letters[c_lower] += 1

    letter_percent = letter_count / total_chars
    if letter_percent > 0.8:
        return True

    return False


def example():
    msg = "hello world"
    key = "a"
    encrypted = string_xor_key(msg, key)
    print(encrypted)
    decrypt = string_xor_key(encrypted, key)
    print("".join(decrypt))


if __name__ == "__main__":
    keys = brute_force_key(hex_string)
    for k in keys:
        print(k[0], "-", k[1])
