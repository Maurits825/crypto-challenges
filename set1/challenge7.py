import base64

from Crypto.Cipher import AES


def decrypt_aes_ecb(binary, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(binary)
    return decrypted_data


if __name__ == "__main__":
    with open("data7.txt", 'rb') as f:
        encrypted_data = f.read()

    b = base64.b64decode(encrypted_data)
    d = decrypt_aes_ecb(b, "YELLOW SUBMARINE".encode('utf-8'))
    print(d)
