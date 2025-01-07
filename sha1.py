import math
from dataclasses import dataclass


@dataclass
class Sha1Register:
    h0_start: int = 0x67452301
    h1_start: int = 0xEFCDAB89
    h2_start: int = 0x98BADCFE
    h3_start: int = 0x10325476
    h4_start: int = 0xC3D2E1F0


block_size = 512 // 8
chunk_size = 32 // 8
mask_32_bit = 0xFFFFFFFF
mask_160_bit = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def rotate_left(value, bits):
    return ((value << bits) | (value >> (32 - bits))) & mask_32_bit


# TODO this padding is wrong when message is exactly the block size
def sha1_pad(message: bytes) -> bytearray:
    ml = len(message)
    block_count = math.floor(ml / block_size) + 1
    b_size = block_count * block_size
    b = bytearray(b_size)
    b[:ml] = message
    b[ml] = 0x80
    b[-8:] = (ml * 8).to_bytes(8, "big")
    return b


def sha1_hash(message: bytes, registers=Sha1Register()):
    b = sha1_pad(message)
    block_count = math.ceil(len(message) / block_size)

    h0 = registers.h0_start
    h1 = registers.h1_start
    h2 = registers.h2_start
    h3 = registers.h3_start
    h4 = registers.h4_start

    blocks = [b[i * block_size:(i + 1) * block_size] for i in range(block_count)]
    for block in blocks:
        w = [
            int.from_bytes(block[i * chunk_size:(i + 1) * chunk_size], "big")
            for i in range(16)
        ]
        for i in range(16, 80):
            w.append(rotate_left(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))

        a, b, c, d, e, f, k = h0, h1, h2, h3, h4, 0, 0

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~ b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = rotate_left(a, 5) + f + e + k + w[i] & mask_32_bit

            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & mask_32_bit
        h1 = (h1 + b) & mask_32_bit
        h2 = (h2 + c) & mask_32_bit
        h3 = (h3 + d) & mask_32_bit
        h4 = (h4 + e) & mask_32_bit

    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return hh & mask_160_bit
