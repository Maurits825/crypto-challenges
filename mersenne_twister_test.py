import unittest

from mersenne_twister import MTRNG


class MersenneTwisterTest(unittest.TestCase):
    def test_same_seed(self):
        seed = 12345
        rng1 = MTRNG(seed)
        rng2 = MTRNG(seed)
        for i in range(100):
            self.assertEqual(rng1.get_random(), rng2.get_random())

    def test_diff_seed(self):
        rng1 = MTRNG(431534)
        rng2 = MTRNG(564803)
        for i in range(10):
            self.assertNotEqual(rng1.get_random(), rng2.get_random())

    def test_no_dupes(self):
        rng = MTRNG(12412124)
        v = [rng.get_random() for _ in range(100)]
        self.assertEqual(len(v), len(set(v)))


if __name__ == '__main__':
    unittest.main()
