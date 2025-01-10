import time
from time import sleep

from sha1 import sha1_hash
from utils import get_random_bytes


class HMACServer:
    def __init__(self):
        self.key = get_random_bytes(100)

    def generate_hash(self, message):
        # todo hmac here
        h = sha1_hash(self.key + message)
        return h.to_bytes(160, "big")

    def validate_hash(self, message, msg_h):
        h = self.generate_hash(message)
        is_valid = self.compare_hash_insecure(msg_h, h)
        return is_valid

    @staticmethod
    def compare_hash(h1, h2):
        return h1

    @staticmethod
    def compare_hash_insecure(h1, h2):
        for b1, b2 in zip(h1, h2):
            if b1 != b2:
                return False
            sleep(0.0005)

        return True


def attack(hmac_server):
    h = hmac_server.generate_hash(b"foo")
    size = len(h)
    message = b"some message"
    forged_hash = bytearray(size)
    for i in range(size):
        diffs = []
        for b in range(0, 255):
            forged_hash[i] = b
            start = time.time()
            is_valid = hmac_server.validate_hash(message, forged_hash)
            end = time.time()
            diff = end - start
            diffs.append((b, diff))

        diffs.sort(key=lambda x: x[1])
        a = 1


def run():
    server = HMACServer()
    attack(server)


if __name__ == "__main__":
    run()
