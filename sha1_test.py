import hashlib
import unittest

from sha1 import sha1_hash


class ShA1TestCase(unittest.TestCase):
    @staticmethod
    def get_sha1_hex(b):
        h = sha1_hash(b)
        s = f"{h:#0{42}x}"
        return s

    @staticmethod
    def get_sha1_hashlib_hex(b):
        m = hashlib.sha1(b)
        s = "0x" + m.hexdigest()
        return s

    def does_hash_same(self, b, msg=None):
        expected = ShA1TestCase.get_sha1_hashlib_hex(b)
        actual = ShA1TestCase.get_sha1_hex(b)
        self.assertEqual(expected, actual, msg)

    def test_sha1_hash(self):
        text_b = b"The quick brown fox jumps over the lazy dog"
        self.does_hash_same(text_b)

    def test_sha1_large_block(self):
        text_b = b"ABCDEF" * 1000
        self.does_hash_same(text_b)

    def test_sha1_exact_block_size(self):
        text_b = b"A" * 64
        self.does_hash_same(text_b)

    def test_sha1_almost_block_size(self):
        text_b = b"A" * 56
        h = sha1_hash(text_b)
        self.does_hash_same(text_b)

    def test_sha1_block_size_0_63(self):
        for i in range(0, 63):
            text_b = b"A" * i
            self.does_hash_same(text_b, "Block size:" + str(i))


if __name__ == '__main__':
    unittest.main()
