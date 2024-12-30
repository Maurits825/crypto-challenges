import unittest

from utils import hex2base64


class MyTestCase(unittest.TestCase):
    def test_hex2base64(self):
        h = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        actual = hex2base64(h)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
