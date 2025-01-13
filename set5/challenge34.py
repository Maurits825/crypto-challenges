from my_crypto import encrypt_cbc, decrypt_cbc, get_dh_coefficient
from sha1 import sha1_hash
from utils import modexp, get_random_bytes

p_nist = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g_nist = 2


def get_key_from_s(s):
    s_b = s.to_bytes(192, "big")
    key = sha1_hash(s_b)
    key_16 = key.to_bytes(20, "big")[:16]
    return key_16


class EchoBot:
    def __init__(self):
        self.p = 0
        self.g = 0
        self.A = 0
        self.key = 0

    def set_params(self, p, g, A):
        self.p = p
        self.g = g
        self.A = A
        b, B = get_dh_coefficient(p, g)
        s = modexp(self.A, b, p)
        self.key = get_key_from_s(s)
        return B

    def echo_encrypt(self, b, iv):
        d = decrypt_cbc(b, iv, self.key)
        iv_new = get_random_bytes(16)
        e = encrypt_cbc(d, iv_new, self.key)
        return e, iv_new


class EchoBotMITM:
    def __init__(self, echo_bot: EchoBot):
        self.echo_bot = echo_bot
        self.key = get_key_from_s(0)

    def set_params(self, p, g, _):
        _ = self.echo_bot.set_params(p, g, p)
        return p

    def echo_encrypt(self, b, iv):
        e, new_iv = self.echo_bot.echo_encrypt(b, iv)
        d = decrypt_cbc(b, iv, self.key)
        print("MITM", d)
        return e, new_iv


def run_protocol(echo_bot):
    p, g = p_nist, g_nist
    a, A = get_dh_coefficient(p, g)
    B = echo_bot.set_params(p, g, A)
    s = modexp(B, a, p)
    key = get_key_from_s(s)

    messages = [b"Hello World!", b"some message", b"foo bar"]
    for msg in messages:
        iv = get_random_bytes(16)
        e = encrypt_cbc(msg, iv, key)
        new_e, new_iv = echo_bot.echo_encrypt(e, iv)
        d = decrypt_cbc(new_e, new_iv, key)
        print(msg, d)


def run():
    print("Normal")
    run_protocol(EchoBot())
    print("MITM")
    run_protocol(EchoBotMITM(EchoBot()))


if __name__ == "__main__":
    run()
