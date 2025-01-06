from sha1 import sha1_hash
from utils import str2bin


def run():
    msg = "foobar text abcd 123 something"
    msg_bin = str2bin(msg)
    h = sha1_hash(bytearray(msg_bin))
    print(h)
    print(hex(h))


if __name__ == "__main__":
    run()
