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

    def test_pad(self):
        text = "YELLOW SUBMARINE"
        b_in = str2bin(text)
        padded = pad(b_in, 20)
        expected = "YELLOW SUBMARINE\x04\x04\x04\x04"
        actual = bin2str(padded)
        self.assertEqual(expected, actual)

        padded = pad(b_in, 19)
        expected = "YELLOW SUBMARINE\x03\x03\x03"
        actual = bin2str(padded)
        self.assertEqual(expected, actual)

    def test_remove_padding(self):
        text = "ICE ICE BABY\x04\x04\x04\x04"
        r_text = bin2str(remove_padding(str2bin(text)))
        expected = "ICE ICE BABY"
        self.assertEqual(expected, r_text)

        text = "ICE ICE BABY\x05\x05\x05\x05"
        b = str2bin(text)
        try:
            remove_padding(b)
        except ValueError:
            pass
        else:
            self.assertEqual(True, False)

        remove_padding(str2bin("FOOO\x01\x01\x02\x02"))
        remove_padding(str2bin("FOO\x01"))
        remove_padding(str2bin("FOO\x02\x02"))
        remove_padding(str2bin("FOO\x03\x03\x03"))
        remove_padding(str2bin("FOO" + ("\x10" * 16)))


if __name__ == '__main__':
    unittest.main()
