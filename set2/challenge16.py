import itertools

from my_crypto import encrypt_cbc, decrypt_cbc
from utils import str2bin, bin2str, get_random_bytes

pre = "comment1=cooking%20MCs;userdata="
post = ";comment2=%20like%20a%20pound%20of%20bacon"


def encrypt(s: str, iv, key):
    # idk
    s = s.replace(";", ":")
    s = s.replace("=", "_")

    final = pre + s + post

    final_bin = str2bin(final)
    e = encrypt_cbc(final_bin, iv, key)
    return e


def find_admin(s: str):
    values = s.split(";")
    for v in values:
        if "admin=true" in v:
            return True
    return False


# works just have to let it cook
# run into either padding errors
# or unicode errors because of the scrambled block
# might be a smarter way to construct the input block
def run():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    pre_length = len(pre)
    # we need the input str to be in its own block
    # so we can scramble it as we wish
    # without corrupting the rest of the data
    target_str = "9admin<true"
    offset = (pre_length % 16)
    input_len = 16 + offset

    d = None
    e = None
    e_tamper = None
    d_str = ""
    input_str = ""
    count = 0
    # i think starting at some value like 90 is better
    # to get better 'bit entropy' if that makes sense
    combinations = itertools.product(range(90, 127), repeat=input_len)
    for c in combinations:
        count += 1
        # input_str = "".join([chr(0 + random.randint(0, 255)) for _ in range(input_len)]) + target_str
        input_str = "".join([chr(i) for i in c]) + target_str
        if count % 1000 == 0:
            print("Count:", count, input_str)

        e = encrypt(input_str, iv, key)
        e_tamper = bytearray(e)
        s_index = pre_length + offset
        e_tamper[s_index] ^= 2
        e_tamper[s_index + 6] ^= 1

        try:
            d = decrypt_cbc(bytes(e_tamper), iv, key)
        except ValueError:
            continue
        try:
            d_str = bin2str(d)
        except UnicodeDecodeError as exc:
            # print(exc)
            continue
        else:
            break

    is_admin = find_admin(d_str)

    print("\nAttack input:", input_str)
    print("Encrypted:", e)
    print("Tampered:", e_tamper)
    print("Decrypted:", d_str)
    print("Is admin:", is_admin)


if __name__ == "__main__":
    run()
