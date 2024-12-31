import base64

from Crypto.Cipher import AES


def decrypt_aes_ecb(input_file, key):
    # Ensure the key is 16 bytes (128 bits)
    if len(key) < 16:
        key = key.ljust(16)  # Pad with spaces if the key is too short
    elif len(key) > 16:
        key = key[:16]  # Truncate if the key is too long

    # Create the cipher object
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)

    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    binary = base64.b64decode(encrypted_data)
    decrypted_data = cipher.decrypt(binary)
    return decrypted_data


if __name__ == "__main__":
    d = decrypt_aes_ecb("data7.txt", "YELLOW SUBMARINE")
    print(d)
