from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class MixedAlphabet(Cipher):

    def __init__(self, key=None):
        self.key = self.validate(key)

    def validate(self, alphabet):
        if alphabet is None:
            alphabet = "QWERTYUIOPASDFG_HJKLZXCVBNM"
        if len(alphabet) != 27:
            raise ScytaleError("The Mixed Alphabet key must be 27 letters long; A-Z plus a space")
        alphabet = alphabet.upper()
        if len(set(alphabet)) != 27:
            raise ScytaleError("The Mixed Alphabet key must have 27 unique letters in it; A-Z plus a space")
        return alphabet

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        return "".join([self.key[self.alphabet.index(c)] for c in plaintext])

    def decrypt(self, ciphertext):
        return "".join([self.alphabet[self.key.index(c)] for c in ciphertext])
