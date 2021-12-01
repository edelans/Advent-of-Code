# Python 3.x

import re

# PART 1


def Input(day):
    "Open this day's input file."
    filename = './input_files/input{}.txt'.format(day)
    return open(filename)


def is_passphrase(words):
    """do these words are a valid passphrase ? (no duplicate words)"""
    return len(words) == len(set(words))


assert is_passphrase("aa bb cc dd ee".split()) is True
assert is_passphrase("aa bb cc dd aa".split()) is False
assert is_passphrase("aa bb cc dd aaa".split()) is True


def parse_words(text):
    "All the words in text"
    return re.findall(r'\w+', text)


def count_valid_passphrases(text):
    passphrases = [parse_words(line) for line in text]
    return sum(map(is_passphrase, passphrases))

# print(count_valid_passphrases(Input(4)))

# PART 2


def sort_letter(word):
    return ''.join(sorted(word))


assert is_passphrase(list(map(sort_letter, "abcde fghij".split()))) is True
assert is_passphrase(list(map(sort_letter, "abcde xyz ecdab".split()))) is False
assert is_passphrase(list(map(sort_letter, "a ab abc abd abf abj".split()))) is True
assert is_passphrase(list(map(sort_letter, "iiii oiii ooii oooi oooo".split()))) is True
assert is_passphrase(list(map(sort_letter, "oiii ioii iioi iiio".split()))) is False


def count_valid_passphrases2(text):
    passphrases = [list(map(sort_letter, parse_words(line))) for line in text]
    return sum(map(is_passphrase, passphrases))

print(count_valid_passphrases2(Input(4)))
