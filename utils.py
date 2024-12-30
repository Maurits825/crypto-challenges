import base64

ENCODE_TYPE = "utf-8"


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
