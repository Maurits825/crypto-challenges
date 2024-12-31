import base64

from my_crypto import decrypt_cbc
from utils import str2bin, bin2str


def decrypt_file():
    with open("data10.txt", 'r') as f:
        encrypted_data = f.read()

    binary = base64.b64decode(encrypted_data)
    iv = bytes(16)
    key = str2bin("YELLOW SUBMARINE")
    decrypt = decrypt_cbc(binary, iv, key)
    print(bin2str(decrypt))


if __name__ == "__main__":
    decrypt_file()
