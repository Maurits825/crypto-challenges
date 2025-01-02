import math

from Crypto.Cipher import AES

from utils import xor_bytes, pad, remove_padding


def encrypt_aes_ecb(binary, key) -> bytes:
    pad_target = math.ceil(len(binary) / 16)
    binary_pad = pad(binary, 16 * pad_target)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(binary_pad)
    return encrypted_data


def decrypt_aes_ecb(binary, key) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(binary)
    return decrypted_data


def encrypt_cbc(binary, iv, key) -> bytes:
    block_size = len(iv)
    cipher_blocks = []
    total_blocks = math.ceil(len(binary) / block_size)
    last_cipher = iv
    for i in range(total_blocks):
        plain_block = binary[i * block_size:(i + 1) * block_size]
        plain_block = pad(plain_block, block_size)
        block = xor_bytes(last_cipher, plain_block)

        cipher = encrypt_aes_ecb(block, key)

        cipher_blocks.append(cipher)
        last_cipher = cipher

    return b''.join(cipher_blocks)


def decrypt_cbc(binary, iv, key) -> bytes:
    block_size = len(iv)
    plain_text_blocks = []
    total_blocks = math.ceil(len(binary) / block_size)
    last_cipher = iv
    for i in range(total_blocks):
        cipher_block = binary[i * block_size:(i + 1) * block_size]
        block = decrypt_aes_ecb(cipher_block, key)
        plain_block = xor_bytes(last_cipher, block)

        plain_text_blocks.append(plain_block)
        last_cipher = cipher_block

    plain_text_blocks[-1] = remove_padding(plain_text_blocks[-1])
    return b''.join(plain_text_blocks)


# TODO mostly works, depends on the plain text though
def detect_ecb(ciphertext, block_size=16):
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) - len(set(blocks))
