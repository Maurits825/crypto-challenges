import random
import time

from mersenne_twister import MTRNG
from my_crypto import encrypt_ctr_prng, create_key_stream_prng
from utils import str2bin, bin2str, xor_bytes


def encrypt_decrypt_ctr_prng():
    text = "Hello World! some text foobar 123abc"
    seed = 0xabcd
    e = encrypt_ctr_prng(str2bin(text), seed)
    d = encrypt_ctr_prng(e, seed)
    d_str = bin2str(d)
    print(d_str, d_str == text)


def brute_force_16bit_seed():
    char = "A"
    p_text_size = 14
    text = "".join([chr(random.randint(0, 50) + 65) for _ in range(random.randint(5, 20))]) + char * p_text_size
    print(text)

    seed = random.randint(0, 2 ** 16 - 1)
    b_in = str2bin(text)
    e = encrypt_ctr_prng(b_in, seed)

    size = len(e)
    seed_guess = None
    p_approximate = str2bin(char * size)
    print("Brute forcing seed...")
    for s in range(2 ** 16):
        if s % 10000 == 0:
            print(s)
        key_stream = create_key_stream_prng(s, size)
        d = xor_bytes(p_approximate, key_stream)
        count = 0
        for b1, b2 in zip(e, d):
            if b1 == b2:
                count += 1
            else:
                count = 0
        if count == p_text_size:
            seed_guess = s
            break

    print("Seed:", seed)
    print("Seed guess:", seed_guess)


def generate_reset_token():
    seed = int(time.time())
    rng = MTRNG(seed)
    r = rng.get_random()
    token = hex(r)  # TODO what to do with r?
    return token, seed


def is_token_from_time_seed(token_raw):
    now = int(time.time())
    # we would need to know how r is used here to make the token?
    token = int(token_raw, 16)
    for i in range(1000):
        s = now - i
        rng = MTRNG(s)
        r = rng.get_random()
        if r == token:
            return s
    return None


def run():
    encrypt_decrypt_ctr_prng()
    print("---")

    token, seed = generate_reset_token()
    seed_guess = is_token_from_time_seed(token)
    print(token, seed, seed_guess, seed == seed_guess)
    print("---")

    brute_force_16bit_seed()


if __name__ == "__main__":
    run()
