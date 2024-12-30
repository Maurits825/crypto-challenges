import base64

ENCODE_TYPE = "utf-8"


def hex2base64(h: str):
    return base64.b64encode(bytes.fromhex(h)).decode(ENCODE_TYPE)


def str2hex(s: str):
    return s.encode(ENCODE_TYPE).hex()


def string_xor_key(s, k_str: str):
    output = []
    k = ord(k_str)
    for i, c in enumerate(s):
        v = ord(c) ^ k
        output.append(chr(v))
    return output
