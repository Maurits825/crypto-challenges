import random
import time

from sha1 import sha1_hash
from utils import get_random_bytes


class HMACServer:
    def __init__(self, is_sim_time=False, sleep_time=0.05):
        self.key = get_random_bytes(100)
        self.key = bytes.fromhex(
            "e1ec2ef0ce7da965a69ac2ab5139ce69bf114cc7ea52ac72cfe564153c2e156e0b500ba0308092eafd36355a2ab0fcedcf1d5a45e28136f77a15bd0868fef2370254c0208e243571a4c7b324d582f914da958fb77e46554ad2cae41321106bc4dc586f4a")

        self.sim_time = 0
        self.is_sim_time = is_sim_time
        self.sleep_time = sleep_time

    def get_time(self):
        if self.is_sim_time:
            return self.sim_time
        else:
            return time.time()

    def generate_hash(self, message):
        # todo hmac here
        h = sha1_hash(self.key + message)
        return h.to_bytes(20, "big")

    def validate_hash(self, message, msg_h):
        h = self.generate_hash(message)
        is_valid = self.compare_hash_insecure(msg_h, h)
        return is_valid

    @staticmethod
    def compare_hash(h1, h2):
        return h1 == h2

    def compare_hash_insecure(self, h1, h2):
        for b1, b2 in zip(h1, h2):
            if b1 != b2:
                return False
            if self.is_sim_time:
                self.sim_time += (self.sleep_time * (random.randint(80, 120) / 100))
            else:
                time.sleep(self.sleep_time)

        return True


def attack(hmac_server):
    h = hmac_server.generate_hash(b"foo")
    size = len(h)
    message = b"some message"
    target_h = hmac_server.generate_hash(message)
    forged_hash = bytearray(size)
    count = 1
    for i in range(size):
        diffs = []
        forged_hash[i:] = get_random_bytes(size - i)
        for b in range(0, 256):
            forged_hash[i] = b
            print("Trying", count, forged_hash, target_h)
            start = hmac_server.get_time()
            is_valid = hmac_server.validate_hash(message, forged_hash)
            end = hmac_server.get_time()
            if is_valid:
                break
            count += 1
            diff = end - start
            # this doenst work if the next byte happens to be 0x00
            d = diff - ((i + 1) * 0.05)
            dd = d ** 2
            if d > 0.001 and b > 5:
                # print("Found", i, bytes(forged_hash), target_h)
                break
            diffs.append(diff)
        else:
            print("Didnt find byte", i, bytes(forged_hash), target_h, hmac_server.key.hex())
            return
        diffs.sort()

    is_valid = hmac_server.validate_hash(message, forged_hash)
    print("Forged hash:", is_valid, count, bytes(forged_hash), message, hmac_server.key.hex())


def run():
    for i in range(1):
        server = HMACServer(is_sim_time=True, sleep_time=0.05)
        attack(server)


if __name__ == "__main__":
    run()
