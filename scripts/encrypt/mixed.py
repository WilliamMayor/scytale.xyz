import random

from scytale.ciphers import MixedAlphabet


if __name__ == '__main__':
    plaintext = input('Plaintext: ')
    key = input('Key: ')
    if not key:
        a = list(MixedAlphabet.alphabet)
        random.shuffle(a)
        key = ''.join(a)
        print(f'Random Key: {key}')
    ciphertext = MixedAlphabet(key=key).encrypt(plaintext)
    print(f'Ciphertext: {ciphertext}')
