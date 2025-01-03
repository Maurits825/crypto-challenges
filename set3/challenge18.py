from my_crypto import encrypt_ctr
from utils import str2bin, bin2str, base642bin


def run():
    text = "Hello World! some text foobar"
    nonce = bytes(8)
    key = str2bin("YELLOW SUBMARINE")
    e = encrypt_ctr(str2bin(text), nonce, key)
    d = encrypt_ctr(e, nonce, key)
    print(bin2str(d))

    input_str = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    b_in = base642bin(input_str)
    d = encrypt_ctr(b_in, nonce, key)
    print(bin2str(d))


if __name__ == "__main__":
    run()
