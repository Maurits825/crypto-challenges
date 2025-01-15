import hashlib
from dataclasses import dataclass

from my_crypto import get_dh_coefficient, hmac
from utils import get_random_bytes, modexp, str2bin

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3


def hash_fn(m):
    return hashlib.sha256(m).hexdigest()


def get_uH(a, b):
    m = (a + b).to_bytes(400, "big")  # TODO
    h = hash_fn(m)
    u = int(h, 16)
    return u


@dataclass
class User:
    email: str
    salt: bytes
    v: int
    k: str = ""


class SRPServer:
    def __init__(self):
        self.users: dict[str, User] = dict()

    def register(self, email, v, salt):
        self.users[email] = User(email, salt, v)

    def get_B_and_salt(self, email, A):
        b, B = get_dh_coefficient(N, g)
        user = self.users[email]
        B = B + k * user.v
        K = SRPServer.get_K(A, B, user.v, b)
        self.users[email].k = K  # TODO...
        return B, user.salt

    def login(self, email, hmac_k):
        user = self.users[email]
        h_fn = lambda m: bytes.fromhex(hash_fn(m))
        h = hmac(str2bin(user.k), user.salt, h_fn)
        is_valid = h == hmac_k
        return is_valid

    @staticmethod
    def get_K(A, B, v, b):
        u = get_uH(A, B)
        base = A * modexp(v, u, N)
        s = modexp(base, b, N)
        s_b = s.to_bytes(192, "big")
        K = hash_fn(s_b)
        return K


class SRPClient:
    def __init__(self, server: SRPServer):
        self.server = server

    def register(self, email, password):
        salt = get_random_bytes(32)
        xH = hash_fn(salt + password)
        x = int(xH, 16)
        v = modexp(g, x, N)
        self.server.register(email, v, salt)

    def login(self, email, password, a_overwrite=None):
        a, A = get_dh_coefficient(N, g)
        if a_overwrite is not None:
            A = a_overwrite
        B, salt = self.server.get_B_and_salt(email, A)
        K = SRPClient.get_K(A, B, a, salt, password)
        h_fn = lambda m: bytes.fromhex(hash_fn(m))
        hmac_k = hmac(str2bin(K), salt, h_fn)
        is_valid = self.server.login(email, hmac_k)
        return is_valid

    @staticmethod
    def get_K(A, B, a, salt, password):
        xH = hash_fn(salt + password)
        x = int(xH, 16)
        b1 = k * modexp(g, x, N)
        b = B - b1
        u = get_uH(A, B)
        e = a + u * x
        s = modexp(b, e, N)
        s_b = s.to_bytes(192, "big")
        K = hashlib.sha256(s_b).hexdigest()
        return K


def attack(email, c):
    for A in [0, N, N ** 2]:
        B, salt = c.server.get_B_and_salt(email, A)
        h_fn = lambda m: bytes.fromhex(hash_fn(m))
        s_b = (0).to_bytes(192, "big")
        h = hash_fn(s_b)
        hmac_k = hmac(str2bin(h), salt, h_fn)
        is_valid = c.server.login(email, hmac_k)
        print("HMAC", is_valid, email, hmac_k.hex())


def run():
    s = SRPServer()
    c = SRPClient(s)
    email = b"foo@bar.com"
    password = b"password"
    c.register(email, password)
    is_valid = c.login(email, password)
    print(is_valid, email, password)

    other_pass = b"abc"
    is_valid = c.login(email, other_pass)
    print(is_valid, email, other_pass)

    attack(email, c)


if __name__ == "__main__":
    run()
