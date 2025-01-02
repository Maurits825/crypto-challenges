from my_crypto import encrypt_aes_ecb, decrypt_aes_ecb
from utils import str2bin, get_random_bytes, bin2str


def parse_string_values(s: str) -> dict[str, str]:
    values = s.split("&")
    d = dict()
    for v in values:
        names = v.split("=")
        d[names[0]] = names[1]
    return d


def profile_for(email: str) -> str:
    assert not ("&" in email or "=" in email)
    user_id = 10  # uuid.uuid1()
    return "email=" + email + "&uid=" + str(user_id) + "&role=user"


def create_admin_profile(key):
    # make an email so that admin+padding is in its own block
    email = "A" * 10 + "admin" + chr(4) * 11
    p = profile_for(email)
    encrypt = encrypt_aes_ecb(str2bin(p), key)
    # the admin+padding is in the second block
    admin_role_encrypt = encrypt[16:32]

    # now make an email so that role= is second last block
    # this assumes that uid is always 2 digits?
    email2 = "A" * 13
    p2 = profile_for(email2)
    encrypt2 = encrypt_aes_ecb(str2bin(p2), key)
    # remove the user role block and paste the admin block
    encrypted_admin = encrypt2[:-16] + admin_role_encrypt

    # check
    d = decrypt_aes_ecb(encrypted_admin, key)
    p_encoded = bin2str(d)
    admin_profile = parse_string_values(p_encoded)
    print(p_encoded, admin_profile)


def run():
    p_str = profile_for("foo@bar.com")

    key = get_random_bytes(16)
    p_encrypted = encrypt_aes_ecb(str2bin(p_str), key)
    p_decrypted = decrypt_aes_ecb(p_encrypted, key)

    p = parse_string_values(bin2str(p_decrypted))
    print(p_str, p)

    create_admin_profile(key)


if __name__ == "__main__":
    run()
