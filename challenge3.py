# from https://cryptopals.com/sets/1/challenges/3
from is_english import is_english
from utils import string_xor_key

hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def brute_force_key(b: iter, score_threshold=10000):
    encrypted = [chr(i) for i in b]
    potential_key = []
    for i in range(5000):  # TODO what is max???
        d = string_xor_key(encrypted, chr(i))
        score = is_english(d)
        if score < score_threshold:
            potential_key.append([chr(i), score])

    potential_key.sort(key=lambda x: x[1])
    return potential_key


def example():
    msg = "hello world"
    key = "a"
    encrypted = string_xor_key(msg, key)
    print(encrypted)
    decrypt = string_xor_key(encrypted, key)
    print("".join(decrypt))


if __name__ == "__main__":
    binary = bytes.fromhex(hex_string)
    keys = brute_force_key(binary)

    chr_msg = [chr(i) for i in binary]
    for k in keys[:2]:
        print(k[0], "-", k[1], "".join(string_xor_key(chr_msg, k[0])))
