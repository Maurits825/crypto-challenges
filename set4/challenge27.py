from my_crypto import encrypt_cbc, decrypt_cbc
from utils import str2bin, get_random_bytes, bin2str

pre = "yellow submarine"
post = "redred submarine"

key = get_random_bytes(16)


def encrypt(s: str):
    s = s.replace(";", ":")
    s = s.replace("=", "_")

    final = pre + s + post

    final_bin = str2bin(final)
    e = encrypt_cbc(final_bin, key, key)
    return e


def decrypt(b):
    d = decrypt_cbc(b, key, key)
    error = False
    for b in d:
        if b < 32:
            error = True
    return error, bin2str(d)


def find_admin(s: str):
    values = s.split(";")
    for v in values:
        if "admin=true" in v:
            return True
    return False


# doesnt totally work because of invalid padding
def attack():
    text = "AABBCCDDEEFF1122"
    e = encrypt(text)
    e_arr = bytearray(e)
    c1 = e_arr[:16]
    e_tamper = c1 + bytearray(16) + c1
    error, d = decrypt(e_tamper)
    p1 = d[:16]
    p2 = d[-16:]
    key_extract = ""
    if error:
        for c1, c2, in zip(p1, p2):
            key_extract += chr(ord(c1) ^ ord(c2))
    print(key_extract)


def run():
    print(bin2str(key))
    attack()


if __name__ == "__main__":
    run()
