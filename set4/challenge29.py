from sha1 import sha1_hash, Sha1Register, sha1_pad

key = b"super secret"


def get_sha1(msg):
    h = sha1_hash(key + msg)
    return h


def run():
    text = b"my message"
    h = get_sha1(text)

    register = Sha1Register(
        (h >> 128) & 0xFFFFFFFF,
        (h >> 96) & 0xFFFFFFFF,
        (h >> 64) & 0xFFFFFFFF,
        (h >> 32) & 0xFFFFFFFF,
        (h >> 0) & 0xFFFFFFFF,
    )
    forged_text_extension = b"forge"
    ml = len(text) + len(key)
    pad_b = bytes(ml)
    glue_pad = sha1_pad(pad_b)[ml:]
    h = sha1_hash(forged_text_extension, register)
    print(hex(h))

    print("---")
    h = get_sha1(text + glue_pad + forged_text_extension)
    print(hex(h))
    h = get_sha1(text + forged_text_extension)
    print(hex(h))


def test():
    m = b"some text"
    m_pad = sha1_pad(m)
    h1 = sha1_hash(m)
    h2 = sha1_hash(m + m_pad[len(m):])
    print(h1 == h2, hex(h1), hex(h2))


if __name__ == "__main__":
    test()
    # run()
