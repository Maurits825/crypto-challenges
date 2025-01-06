from sha1 import sha1_hash


def run():
    secret = b"super secret"
    msg = b"foobar text abcd 123 something"
    h = sha1_hash(secret + msg)
    print(hex(h))

    h = sha1_hash(secret + msg + b"more")
    print(hex(h))

    msg = b"foobar text abcd 124 something"
    h = sha1_hash(secret + msg)
    print(hex(h))


if __name__ == "__main__":
    run()
