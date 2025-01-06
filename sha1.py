import math

h0_start = 0x67452301
h1_start = 0xEFCDAB89
h2_start = 0x98BADCFE
h3_start = 0x10325476
h4_start = 0xC3D2E1F0

block_size = 512 // 8
chunk_size = 32 // 8
mask_32_bit = 0xFFFFFFFF
mask_160_bit = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


def sha1_hash(message: bytes):
    ml = len(message)
    block_count = math.ceil(ml / block_size)
    b_size = block_count * block_size
    b = bytearray(b_size)
    b[:ml] = message
    b[ml] = 1
    b[-8:] = ml.to_bytes(8, "big")

    h0 = h0_start
    h1 = h1_start
    h2 = h2_start
    h3 = h3_start
    h4 = h4_start

    blocks = [b[i * block_size:(i + 1) * block_size] for i in range(block_count)]
    for block in blocks:
        w = [
            int.from_bytes(block[i * chunk_size:(i + 1) * chunk_size], "big")
            for i in range(16)
        ]
        for i in range(16, 79):
            v = (w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]) << 1
            w.append(v & mask_32_bit)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = 0
        k = 0

        for i in range(0, 79):
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

            temp = (a << 5) + f + e + k + w[i]

            e = d & mask_32_bit
            d = c & mask_32_bit
            c = (b << 30) & mask_32_bit
            b = a & mask_32_bit
            a = temp & mask_32_bit

        h0 = h0 + a
        h1 = h1 + b
        h2 = h2 + c
        h3 = h3 + d
        h4 = h4 + e

    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return hh & mask_160_bit
