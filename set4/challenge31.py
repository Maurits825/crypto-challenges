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
                self.sim_time += (self.sleep_time * (random.randint(99, 101) / 100))
            else:
                time.sleep(self.sleep_time)

        return True


def attack(hmac_server):
    valid_hash = hmac_server.generate_hash(b"")
    size = len(valid_hash)
    message = b"some message"
    target_h = hmac_server.generate_hash(message)
    forged_hash = bytearray(size)
    test_h = bytearray(size)
    count = 1
    test_count = 10
    for i in range(size):
        average_t = 0
        test_h[:] = valid_hash
        if i + 1 < size:
            test_h[i + 1] ^= 1
        for _ in range(test_count):
            start = hmac_server.get_time()
            _ = hmac_server.validate_hash(b"", test_h)
            end = hmac_server.get_time()
            diff = end - start
            average_t += diff
        average_t /= test_count
        average_byte_sleep = average_t / (i + 1)
        tolerance = abs((1 / (2 * i - 1)) * 0.8)
        threshold = average_t - (tolerance * average_byte_sleep)

        eta = 0
        for j in range(i, size):
            eta += (256 / 2) * average_byte_sleep * j

        print("Byte/Tries", i, count, int(eta))
        highest_t = 0
        highest_b = 0
        for b in range(0, 256):
            forged_hash[i] = b
            # print("Trying", count, forged_hash, target_h)
            start = hmac_server.get_time()
            is_valid = hmac_server.validate_hash(message, forged_hash)
            end = hmac_server.get_time()
            if is_valid:
                break
            count += 1
            diff = end - start
            if diff > highest_t:
                highest_t = diff
                highest_b = b
            d = diff - ((i + 1) * 0.05)
            d2 = (diff - average_t) / average_t
            if diff > threshold:
                # print("Found", i, bytes(forged_hash), target_h)
                if b != target_h[i]:
                    print("incorrect match", highest_t, average_t, threshold)
                else:
                    break

        else:
            print("Didnt find byte", i, bytes(forged_hash), target_h, hmac_server.key.hex())
            print("Trying Best guess", chr(highest_b), chr(target_h[i]), highest_t, average_t, threshold)
            if highest_b != target_h[i]:
                print("Bad guess")
                return
            forged_hash[i] = highest_b

    is_valid = hmac_server.validate_hash(message, forged_hash)
    print("Forged hash:", is_valid, count, bytes(forged_hash), message, hmac_server.key.hex())


def run():
    for i in range(1):
        is_sim = True
        server = HMACServer(is_sim_time=is_sim, sleep_time=0.001)
        attack(server)
        if is_sim:
            print("Server time min", server.get_time() // 60)


if __name__ == "__main__":
    run()
