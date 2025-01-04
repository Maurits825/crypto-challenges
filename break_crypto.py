import itertools
import math

from is_english import is_english
from utils import bin2str


def break_repeating_xor(b_in: bytes, key_size, score_threshold=1000) -> list[bytearray]:
    assert len(b_in) % key_size == 0

    block_len = int(len(b_in) / key_size)
    transpose = [bytearray(block_len) for _ in range(key_size)]
    for i, v in enumerate(b_in):
        transpose[i % key_size][math.floor(i / key_size)] = v

    current_bytes = bytearray(block_len)
    key_matches = [[] for _ in range(key_size)]
    for key_index, block in enumerate(transpose):
        for k in range(255):
            for i, b in enumerate(block):
                current_bytes[i] = b ^ k
            plain_text = bin2str(current_bytes)
            score = is_english(plain_text)
            if score < score_threshold:
                key_matches[key_index].append((k, score))
        key_matches[key_index].sort(key=lambda x: x[1])

    # todo doesnt do anything rn, with big keysize cant really do this
    combinations = itertools.product(range(0, 1), repeat=key_size)
    keys = []
    for c in combinations:
        k = bytearray([key_matches[i][c[i]][0] for i in range(key_size)])
        keys.append(k)

    return keys
