n = 624
m = 397
w = 32
r = 31
UMASK = 0xffffffff << r
LMASK = 0xffffffff >> (w - r)
a = 0x9908b0df
u = 11
s = 7
t = 15
l = 18
b = 0x9d2c5680
c = 0xefc60000
f = 1812433253


class MTRNG:
    def __init__(self, seed=19650218):
        self.state_array = [0] * n
        self.state_index = 0

        self.state_array[0] = seed
        for i in range(1, n):
            seed = f * (seed ^ (seed >> (w - 2))) + i
            seed = seed & 0xFFFFFFFF
            self.state_array[i] = seed

    def get_random(self):
        k = self.state_index
        j = k - (n - 1)
        if j < 0:
            j += n

        x = (self.state_array[k] & UMASK) | (self.state_array[j] & LMASK)
        xA = x >> 1
        if x & 0x00000001:
            xA ^= a

        j = k - (n - m)
        if j < 0:
            j += n

        x = self.state_array[j] ^ xA
        self.state_array[k] = x
        k += 1

        if k >= n:
            k = 0

        self.state_index = k

        y = x ^ (x >> u)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)

        z = y ^ (y >> l)
        return z
