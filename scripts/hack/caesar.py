import sys
import time

from scytale.ciphers import Caesar


def hack(ciphertext, slow=False):
    print('Hacking...')
    with open('/usr/src/app/scripts/hack/words.txt') as word_file:
        words = set(word.strip().upper() for word in word_file)
    best_match = (0, 0, '')
    for key in range(27):
        c = Caesar(key=key)
        plaintext = c.decrypt(ciphertext)
        print(f'\x1b[2K  Trying key: {key}', end='\r')
        possible_words = set(plaintext.replace('_', ' ').split(' '))
        matches = len(words.intersection(possible_words))
        if matches > best_match[0]:
            best_match = (matches, key, plaintext)
        if slow:
            time.sleep(0.5)
    print(f'\n\n      Key: {best_match[1]}')
    print(f'Plaintext: {best_match[2]}', end='\n\n')


if __name__ == '__main__':
    ciphertext = input('Ciphertext: ').upper().replace(' ', '_')
    hack(ciphertext, slow=len(sys.argv) > 1)
