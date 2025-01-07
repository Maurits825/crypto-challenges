import hashlib
import unittest

from sha1 import sha1_hash


class ShA1TestCase(unittest.TestCase):
    def test_sha1_hash(self):
        text_b = b"The quick brown fox jumps over the lazy dog"
        h = sha1_hash(text_b)
        actual = hex(h)
        expected = "0x2fd4e1c67a2d28fced849ee1bb76e7391b93eb12"
        self.assertEqual(expected, actual)

    def test_sha1_w_hashlib(self):
        text_b = b"Some text to hash foobar 123!"
        h = sha1_hash(text_b)
        actual = hex(h)
        m = hashlib.sha1(text_b)
        expected = "0x" + m.hexdigest()
        self.assertEqual(expected, actual)

    def test_sha1_large_block(self):
        text_b = b"ABCDEF" * 100
        h = sha1_hash(text_b)
        actual = hex(h)
        m = hashlib.sha1(text_b)
        expected = "0x" + m.hexdigest()
        self.assertEqual(expected, actual)

    def test_sha1_exact_block_size(self):
        text_b = b"A" * 64
        h = sha1_hash(text_b)
        actual = hex(h)
        m = hashlib.sha1(text_b)
        expected = "0x" + m.hexdigest()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
