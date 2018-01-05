import math
import time
import itertools

from scytale.ciphers import MixedAlphabet


def hack(ciphertext):
    print('Hacking...')
    with open('/usr/src/app/scripts/hack/words.txt') as word_file:
        words = set(word.strip().upper() for word in word_file)
    best_match = (0, 0, '')
    guesses = 0
    try:
        tick = time.time()
        for key in itertools.permutations(list(MixedAlphabet.alphabet)):
            key = ''.join(key)
            c = MixedAlphabet(key=key)
            plaintext = c.decrypt(ciphertext)
            print(f'\x1b[2K  Trying key: {key}', end='\r')
            possible_words = set(plaintext.replace('_', ' ').split(' '))
            matches = len(words.intersection(possible_words))
            if matches > best_match[0]:
                best_match = (matches, key, plaintext)
            guesses += 1
        print(f'\n\n      Key: {best_match[1]}')
        print(f'Plaintext: {best_match[2]}', end='\n\n')
    except KeyboardInterrupt:
        tock = time.time()
        seconds = int(tock - tick)
        print(f'\n\nTried {guesses} guesses in {seconds} seconds')
        more = guesses / seconds * math.factorial(27)
        print(f'Need {more:.2E} more seconds to finish')
        hours = more / 60 / 60
        print(f' - {hours:.2E} hours')
        days = hours / 24
        print(f' - {days:.2E} days')
        years = days / 365
        print(f' - {years:.2E} years')
        uni_lifetimes = years / 13.8E+9
        print(f' - {uni_lifetimes:.2E} universe lifetimes')
        sheets_of_paper_to_moon = 400000000 / 0.0001  # Distance to moon (meters) over thickness of paper
        times_to_moon = years / sheets_of_paper_to_moon  # One sheet of paper a year
        print(f' - {times_to_moon:.2E} ttmop')
        times_to_moon_and_back = 2 * times_to_moon / sheets_of_paper_to_moon  # One sheet of paper everytime you get to the moon
        print(f' - {times_to_moon_and_back:.2f} ttmabop')


if __name__ == '__main__':
    ciphertext = input('Ciphertext: ').upper().replace(' ', '_')
    hack(ciphertext)
