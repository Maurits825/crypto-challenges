import hashlib
import random

from md4 import MD4, MD4Register
from utils import get_random_bytes

key = get_random_bytes(random.randint(5, 50))


def get_server_sha(msg):
    h = hashlib.new('md4', key + msg)
    return h.hexdigest()


def is_valid_hash(m, h):
    sh = get_server_sha(m)
    return sh == h


def attack() -> (bytes, int):
    # TODO does it matter that the forged msg will have random garbage from glue padding
    forged_text = b";admin=true;"
    msg_start = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    h = get_server_sha(msg_start)

    r = []
    packed_hash = bytes.fromhex(h)
    for i in range(0, len(packed_hash), 4):
        value = (
                packed_hash[i] |
                (packed_hash[i + 1] << 8) |
                (packed_hash[i + 2] << 16) |
                (packed_hash[i + 3] << 24)
        )
        r.append(value)
    register = MD4Register(
        r[0],
        r[1],
        r[2],
        r[3],
    )

    m_start_len = len(msg_start)
    for key_size in range(1, 100):
        ml = m_start_len + key_size
        pad_b = bytes(ml)
        glue_pad = MD4.pad(pad_b, ml * 8)[ml:]
        forged_message = msg_start + glue_pad + forged_text
        ml_overwrite = 8 * (len(forged_message) + key_size)
        forged_hash = MD4(forged_text, register, ml_overwrite).hexdigest()
        is_valid = is_valid_hash(forged_message, forged_hash)
        print("Tried", ml, forged_hash, is_valid)
        if is_valid:
            return forged_message, forged_hash
    return None, None


def run():
    m, h = attack()
    print("\nForged message:", m)
    print("Forged hash:", h)
    print("Server hash:", get_server_sha(m))


if __name__ == "__main__":
    run()
