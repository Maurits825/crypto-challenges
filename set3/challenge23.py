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
    state_array = []
    for i in range(624):
        r = rng.get_random()
        x = untemper(r)
        state_array.append(x)

    rng_dupe = MTRNG()
    rng_dupe.set_state_array(state_array)
    for i in range(1000):
        r1 = rng.get_random()
        r2 = rng_dupe.get_random()
        print(r1 == r2, r1, r2)


if __name__ == "__main__":
    run()
