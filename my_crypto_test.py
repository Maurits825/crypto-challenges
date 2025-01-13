import hashlib
import unittest

from my_crypto import encrypt_aes_ecb, decrypt_aes_ecb, encrypt_cbc, decrypt_cbc, hmac
from sha1 import sha1_hash
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

    def test_hmac(self):
        key = b"key"
        msg = b"The quick brown fox jumps over the lazy dog"
        hash_fn = lambda m: sha1_hash(m).to_bytes(20, "big")
        actual = hmac(key, msg, hash_fn)
        expected = "de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9"
        self.assertEqual(expected, actual.hex())

        hash_fn = lambda m: bytes.fromhex(hashlib.sha256(m).hexdigest())
        actual = hmac(key, msg, hash_fn)
        expected = "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
        self.assertEqual(expected, actual.hex())


if __name__ == '__main__':
    unittest.main()
