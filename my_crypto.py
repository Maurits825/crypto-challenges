import math

from Crypto.Cipher import AES

from utils import xor_bytes, pad, remove_padding


# TODO there lots of dupe empty padding...
def encrypt_aes_ecb(binary, key) -> bytes:
    pad_target = math.ceil(len(binary) / 16)
    binary_pad = pad(binary, 16 * pad_target)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(binary_pad)
    return encrypted_data


def decrypt_aes_ecb(binary, key, is_remove_pad=False) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(binary)

    if is_remove_pad:
        decrypted_data = remove_padding(decrypted_data)
    return decrypted_data


def encrypt_cbc(binary_in, iv, key) -> bytes:
    block_size = len(iv)
    pad_target = 1 + math.floor(len(binary_in) / block_size)
    binary = pad(binary_in, block_size * pad_target)
    total_blocks = math.ceil(len(binary) / block_size)

    last_cipher = iv
    cipher_blocks = []
    for i in range(total_blocks):
        plain_block = binary[i * block_size:(i + 1) * block_size]
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


def create_key_stream(key, nonce, size) -> bytearray:
    counter = 0
    key_stream_len = math.ceil(size / 16)
    key_stream = bytes()
    for i in range(key_stream_len):
        d = nonce + counter.to_bytes(8, byteorder="little")
        e = encrypt_aes_ecb(d, key)
        key_stream = key_stream + e
        counter += 1

    key_stream = bytearray(key_stream)
    return key_stream[:size]


def encrypt_ctr(binary, nonce, key) -> bytes:
    key_stream = create_key_stream(key, nonce, len(binary))
    cipher = xor_bytes(binary, key_stream)
    return cipher


# TODO mostly works, depends on the plain text though
def detect_ecb(ciphertext, block_size=16):
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) - len(set(blocks))
