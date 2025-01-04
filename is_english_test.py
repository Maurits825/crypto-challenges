import unittest

from is_english import is_english


class IsEnglish(unittest.TestCase):
    def test_is_english(self):
        s = "=76-'9<02  2#2 '9 9=<'=789- 5$9;6-=:-#?;7= ''==6''52S'&S-5 5"
        score = is_english(s)
        self.assertTrue(score > 1000)

        s = "Hello World! This should be english text, but what score?"
        score = is_english(s)
        self.assertTrue(score < 500)


if __name__ == '__main__':
    unittest.main()
