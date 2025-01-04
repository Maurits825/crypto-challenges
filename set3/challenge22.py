import random
import time
from time import sleep

from mersenne_twister import MTRNG


def attack(r):
    print("Attack")
    now = int(time.time())
    for i in range(10000):
        if i % 1000 == 0:
            print(i)
        seed = now - i
        rng = MTRNG(seed)
        v = rng.get_random()
        if r == v:
            return seed
    return 0


def create_random():
    print("Sleeping... ")
    sleep(random.randint(20, 60))

    seed = int(time.time())
    rng = MTRNG(seed)

    print("Sleeping again... ")
    sleep(random.randint(20, 60))

    r = rng.get_random()
    return r, seed


def run():
    r, seed = create_random()
    guess = attack(r)
    print(r, seed, guess)


if __name__ == "__main__":
    run()
