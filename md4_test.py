import hashlib
import unittest

from md4 import MD4


class MD4TestCase(unittest.TestCase):
    @staticmethod
    def get_md4_hex(b):
        h = MD4(b)
        return h.hexdigest()

    @staticmethod
    def get_md4_hashlib_hex(b):
        h = hashlib.new('md4', b)
        return h.hexdigest()

    def does_hash_same(self, b, msg=None):
        expected = MD4TestCase.get_md4_hashlib_hex(b)
        actual = MD4TestCase.get_md4_hex(b)
        self.assertEqual(expected, actual, msg)

    def test_md4_hash(self):
        text_b = b"The quick brown fox jumps over the lazy dog"
        self.does_hash_same(text_b)

    def test_md4_fuzz(self):
        for i in range(0, 100):
            text_b = b"A" * i
            self.does_hash_same(text_b, "Block size:" + str(i))


if __name__ == '__main__':
    unittest.main()
