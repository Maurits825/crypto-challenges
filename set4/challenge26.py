from my_crypto import encrypt_ctr
from utils import str2bin, get_random_bytes, bin2str

pre = "comment1=cooking%20MCs;userdata="
post = ";comment2=%20like%20a%20pound%20of%20bacon"

nonce = bytes(8)
key_ctr = get_random_bytes(16)


def encrypt(s: str):
    s = s.replace(";", ":")
    s = s.replace("=", "_")

    final = pre + s + post

    final_bin = str2bin(final)
    e = encrypt_ctr(final_bin, nonce, key_ctr)
    return e


def decrypt(b):
    d = encrypt_ctr(b, nonce, key_ctr)
    return bin2str(d)


def find_admin(s: str):
    values = s.split(";")
    for v in values:
        if "admin=true" in v:
            return True
    return False


def attack():
    pre_length = len(pre)
    target_text = "A;admin=true"
    target_len = len(target_text)

    tap_text = "A" * target_len
    e = bytearray(encrypt(tap_text))
    target_e_bytes = bytearray(target_len)
    for i in range(target_len):
        k = e[i + pre_length] ^ ord(tap_text[i])
        target_e_bytes[i] = k ^ ord(target_text[i])

    e[pre_length:pre_length + target_len] = target_e_bytes
    return tap_text, e


def run():
    text = "comment;admin=true"
    e = encrypt(text)
    d = decrypt(e)

    print("Input:", text)
    print("Encoded:", d)
    print("Is admin:", find_admin(d))

    print("---")

    attack_input, e_tampered = attack()
    d = decrypt(e_tampered)
    print("Input:", attack_input)
    print("Encoded:", d)
    print("Is admin:", find_admin(d))


if __name__ == "__main__":
    run()
