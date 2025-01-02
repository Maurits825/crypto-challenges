import base64
import random

ENCODE_TYPE = "utf-8"


def bin2str(b: bytes) -> str:
    return b.decode(ENCODE_TYPE)


def base642bin(s: str) -> bytes:
    return base64.b64decode(s)


def str2bin(s: str) -> bytes:
    return s.encode(ENCODE_TYPE)


def hex2base64(h: str):
    return base64.b64encode(bytes.fromhex(h)).decode(ENCODE_TYPE)


def str2hex(s: str):
    return s.encode(ENCODE_TYPE).hex()


def get_hamming_distance_str(s1: str, s2: str) -> int:
    b1 = [ord(s) for s in s1]
    b2 = [ord(s) for s in s2]

    return get_hamming_distance(b1, b2)


def get_hamming_distance(s1: iter, s2: iter) -> int:
    assert len(s1) == len(s2)
    s_len = (len(s1))
    d = 0
    for i in range(s_len):
        xor = s1[i] ^ s2[i]
        # TODO this is prob very slow/scuffed
        str_bin = format(xor, "b")
        for b in str_bin:
            if b == "1":
                d += 1
    return d


def string_xor_key(s, k_str: str):
    output = []
    k = ord(k_str)
    for i, c in enumerate(s):
        v = ord(c) ^ k
        output.append(chr(v))
    return output


def pad(b_in: bytes, target_size: int) -> bytes:
    pad_count = target_size - len(b_in)
    assert pad_count >= 0  # deal later to cut off then?
    padded = bytearray([pad_count for _ in range(target_size)])
    for i, b in enumerate(b_in):
        padded[i] = b
    return padded


def remove_padding(b: bytes) -> bytes:
    p_count = 0
    for i in range(len(b) - 1, 0, -1):
        if b[i] != b[i - 1]:
            p_count += 1
            break
        p_count += 1

    if p_count > 0:
        if b[-1] != p_count:
            raise ValueError("Invalid padding")

    return b[:-p_count]


def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    size = len(b1)
    assert size == len(b2)
    xor_b = bytearray(size)
    for i in range(size):
        xor_b[i] = b1[i] ^ b2[i]
    return bytes(xor_b)


def get_random_bytes(size) -> bytes:
    r = bytearray(size)
    for i in range(size):
        r[i] = int(random.random() * 256)
    return r
