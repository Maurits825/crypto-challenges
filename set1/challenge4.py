from challenge3 import brute_force_key


def find_encrypted_str():
    with open("data4.txt", 'r') as file:
        for line in file:
            keys = brute_force_key(line)
            if len(keys) > 0:
                print("Found:")
                print(line)
                print(keys)
                print("-----")


if __name__ == "__main__":
    find_encrypted_str()
