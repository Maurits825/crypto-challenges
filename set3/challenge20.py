from break_crypto import break_repeating_xor
from my_crypto import encrypt_ctr
from utils import base642bin, get_random_bytes, xor_bytes, bin2str


def attack(encrypted):
    cipher = bytes()
    min_len = min([len(e) for e in encrypted])
    for e in encrypted:
        cipher = cipher + e[:min_len]

    keys = break_repeating_xor(cipher, min_len)
    for k in keys[:2]:
        for e in encrypted:
            d = xor_bytes(k, e[:min_len])
            d_str = bin2str(d)
            print(d_str)


def run():
    nonce = bytes(8)
    key = get_random_bytes(16)
    encrypted = []
    with open("data20.txt", 'r') as file:
        for line in file:
            b = base642bin(line)
            e = encrypt_ctr(b, nonce, key)
            encrypted.append(bytearray(e))

    attack(encrypted)


if __name__ == "__main__":
    run()
