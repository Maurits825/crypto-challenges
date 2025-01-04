alphabet = 'abcdefghijklmnopqrstuvwxyz '
target_frequency = {
    "e": 11.1607,
    "m": 3.0129,
    "a": 8.4966,
    "h": 3.0034,
    "r": 7.5809,
    "g": 2.4705,
    "i": 7.5448,
    "b": 2.0720,
    "o": 7.1635,
    "f": 1.8121,
    "t": 6.9509,
    "y": 1.7779,
    "n": 6.6544,
    "w": 1.2899,
    "s": 5.7351,
    "k": 1.1016,
    "l": 5.4893,
    "v": 1.0074,
    "c": 4.5388,
    "x": 0.2902,
    "u": 3.6308,
    "z": 0.2722,
    "d": 3.3844,
    "j": 0.1965,
    "p": 3.1671,
    "q": 0.1962,
    " ": 20.0,
}

other_chars = "',.!?"


def is_english(chars) -> float:
    total_chars = len(chars)
    letter_count = 0
    other_char_count = 0
    letters = dict()
    for c in chars:
        c_lower = c.lower()
        if c_lower in alphabet:
            letter_count += 1
            if c_lower not in letters:
                letters[c_lower] = 0
            else:
                letters[c_lower] += 1
        elif c_lower in other_chars:
            other_char_count += 1

    score = 0
    alphabet_f = letter_count / total_chars
    if alphabet_f <= 0.2:
        return float("inf")

    for letter in letters:
        letter_percent = (letters[letter] / letter_count) * 100
        diff = abs(letter_percent - target_frequency[letter]) ** 2
        score += diff

    score = score / (alphabet_f ** 4)
    # todo do something more here? basically no impact
    score = score - other_char_count
    return score


if __name__ == "__main__":
    s = is_english("Cooking MC's like a pound of bacon")
    print(s)
