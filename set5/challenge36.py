import hashlib

from my_crypto import get_dh_coefficient, hmac
from utils import get_random_bytes, modexp

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3
email = b"foo@bar.com"
password = b"password"


def hash_fn(m):
    return hashlib.sha256(m).hexdigest()


def get_uH(a, b):
    m = (a + b).to_bytes(400, "big")  # TODO
    h = hash_fn(m)
    u = int(h, 16)
    return u


class SRPServer:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.b = 0

        self.salt = get_random_bytes(32)
        xH = hash_fn(self.salt + password)
        x = int(xH, 16)
        self.v = modexp(g, x, N)

    def set_A(self, A):
        self.A = A
        self.b, self.B = get_dh_coefficient(N, g)
        self.B = self.B + k * self.v  # TODO is this right? or mod N again?
        return self.salt, self.B

    def get_K(self):
        u = get_uH(self.A, self.B)
        base = self.A * modexp(self.v, u, N)
        s = modexp(base, self.b, N)
        s_b = s.to_bytes(192, "big")
        K = hash_fn(s_b)
        return K

    def validate_salt_hash(self, h):
        K = bytes.fromhex(self.get_K())
        h_fn = lambda m: bytes.fromhex(hash_fn(m))
        h1 = hmac(K, self.salt, h_fn)
        return h == h1


class SRPClient:
    def __init__(self, server: SRPServer):
        self.server = server
        self.a, self.A = get_dh_coefficient(N, g)
        self.salt, self.B = self.server.set_A(self.A)

    def get_K(self):
        xH = hash_fn(self.salt + password)
        x = int(xH, 16)
        b1 = k * modexp(g, x, N)
        b = self.B - b1
        u = get_uH(self.A, self.B)
        e = self.a + u * x
        s = modexp(b, e, N)
        s_b = s.to_bytes(192, "big")
        K = hashlib.sha256(s_b).hexdigest()
        return K

    def validate_server(self):
        K = bytes.fromhex(self.get_K())
        h_fn = lambda m: bytes.fromhex(hash_fn(m))
        h = hmac(K, self.salt, h_fn)
        return self.server.validate_salt_hash(h)


def run():
    s = SRPServer()
    c = SRPClient(s)
    k1 = s.get_K()
    k2 = c.get_K()
    print(k1 == k2, k1, k2)
    print(c.validate_server())


if __name__ == "__main__":
    run()
