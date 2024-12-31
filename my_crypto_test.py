import unittest

from my_crypto import encrypt_aes_ecb, decrypt_aes_ecb, encrypt_cbc, decrypt_cbc
from utils import str2bin


class MyTestCase(unittest.TestCase):
    def test_encrypt_decrypt(self):
        b_in = bytes.fromhex("aabbccddaabbccddaabbccddaabbccdd")
        key = str2bin("YELLOW SUBMARINE")
        encrypt = encrypt_aes_ecb(b_in, key)
        decrypt = decrypt_aes_ecb(encrypt, key)
        self.assertEqual(b_in, decrypt)

    def test_encrypt_decrypt_cbc(self):
        b_in = str2bin("Hello world! Some text to encrypt!! foobar")
        key = str2bin("YELLOW SUBMARINE")
        iv = bytes.fromhex("aabbccddaabbccddaabbccddaabbccdd")
        encrypt = encrypt_cbc(b_in, iv, key)
        decrypt = decrypt_cbc(encrypt, iv, key)
        self.assertEqual(b_in, decrypt)


if __name__ == '__main__':
    unittest.main()
