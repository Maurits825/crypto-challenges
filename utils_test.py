import unittest

from utils import *


class MyTestCase(unittest.TestCase):
    def test_hex2base64(self):
        h = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        actual = hex2base64(h)
        self.assertEqual(expected, actual)

    def test_get_hamming_distance(self):
        s1 = "this is a test"
        s2 = "wokka wokka!!!"
        d = get_hamming_distance_str(s1, s2)
        self.assertEqual(37, d)


if __name__ == '__main__':
    unittest.main()
