from utils import str2hex


def repeating_xor_encrypt(msg: str, key: str):
    output = []
    key_len = len(key)
    for i, c in enumerate(msg):
        v = ord(c) ^ ord(key[i % key_len])
        output.append(chr(v))
    return output


if __name__ == "__main__":
    msg = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
    key = "ICE"
    e = repeating_xor_encrypt(msg, key)
    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    # todo some \n char diff?
    print(e == expected)
    print(str2hex("".join(e)))
