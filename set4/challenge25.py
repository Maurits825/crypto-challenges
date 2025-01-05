import base64

from my_crypto import decrypt_aes_ecb, encrypt_ctr
from utils import str2bin, get_random_bytes, bin2str, xor_bytes

nonce = bytes(8)
key_ctr = get_random_bytes(16)


def run():
    e = encrypt_file_ctr()
    e_edit = edit_cipher(e, 3, "edited text!")
    d = encrypt_ctr(e_edit, nonce, key_ctr)
    print(bin2str(d)[:20])
    print("---")
    attack(e)


def attack(original_cipher):
    char = "A"
    key_stream = []
    size = len(original_cipher)
    for i in range(size):
        if i % 100 == 0:
            print(i, "/", size)
        e = bytearray(edit_cipher(original_cipher, i, char))
        k = e[i] ^ ord(char)
        key_stream.append(k)

    d = xor_bytes(original_cipher, bytearray(key_stream))
    print(bin2str(d))


def edit_cipher(cipher, offset, new_text):
    d = bytearray(encrypt_ctr(cipher, nonce, key_ctr))
    d[offset:len(new_text)] = str2bin(new_text)
    e = encrypt_ctr(d, nonce, key_ctr)
    return e


def encrypt_file_ctr():
    with open("../set1/data7.txt", 'rb') as f:
        encrypted_data = f.read()

    b = base64.b64decode(encrypted_data)
    key = str2bin("YELLOW SUBMARINE")
    d = decrypt_aes_ecb(b, key)

    e = encrypt_ctr(d, nonce, key_ctr)
    return e


if __name__ == "__main__":
    run()
