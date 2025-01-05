import time

from mersenne_twister import MTRNG

u = 11
s = 7
t = 15
l = 18
b = 0x9d2c5680
c = 0xefc60000
f = 1812433253


def temper(x):
    y = x ^ (x >> u)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    z = y ^ (y >> l)
    return z


def test():
    y = 0xa1b2c3d4
    z = y ^ (y >> u)

    y = z & ((2 ** u - 1) << u)
    y = z ^ (y >> u)
    y = z ^ (y >> u)
    y = z ^ (y >> u)
    print(hex(y))


def untemper(z):
    y_upper = z & (0x3ffff << l)
    y = z ^ (y_upper >> l)

    z = y
    y = z & 0x7fff
    for i in range(2):
        y = z ^ ((y << t) & c)

    z = y
    y = z & ((2 ** s) - 1)
    for i in range(4):
        y = z ^ ((y << s) & b)

    z = y
    y = z & ((2 ** u - 1) << u)
    for i in range(3):
        y = z ^ (y >> u)

    return y


def run():
    seed = int(time.time())
    rng = MTRNG(seed)

    x = rng.get_random()
    y = temper(x)
    x_re = untemper(y)
    print(x, y, x_re, x == x_re)


if __name__ == "__main__":
    run()
