import hashlib
import random

from sha1 import sha1_hash, Sha1Register, sha1_pad
from utils import get_random_bytes

key = get_random_bytes(random.randint(5, 50))


def get_server_sha(msg):
    h = hashlib.sha1(key + msg)
    return int(h.hexdigest(), 16)


def is_valid_hash(m, h):
    return get_server_sha(m) == h


def attack() -> (bytes, int):
    # TODO does it matter that the forged msg will have random garbage from glue padding
    forged_text = b";admin=true;"
    msg_start = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    h = get_server_sha(msg_start)

    register = Sha1Register(
        (h >> 128) & 0xFFFFFFFF,
        (h >> 96) & 0xFFFFFFFF,
        (h >> 64) & 0xFFFFFFFF,
        (h >> 32) & 0xFFFFFFFF,
        (h >> 0) & 0xFFFFFFFF,
    )
    m_start_len = len(msg_start)
    for key_size in range(100):
        ml = m_start_len + key_size
        pad_b = bytes(ml)
        glue_pad = sha1_pad(pad_b)[ml:]
        forged_message = msg_start + glue_pad + forged_text
        ml_overwrite = 8 * (len(forged_message) + len(key))
        forged_hash = sha1_hash(forged_text, register, ml_overwrite)
        is_valid = is_valid_hash(forged_message, forged_hash)
        print("Trying", ml, hex(forged_hash), is_valid)
        if is_valid:
            return forged_message, forged_hash
    return None, None


def run():
    m, h = attack()
    print("\nForged message:", m)
    print("Forged hash:", hex(h))
    print("Server hash:", hex(get_server_sha(m)))


if __name__ == "__main__":
    run()
