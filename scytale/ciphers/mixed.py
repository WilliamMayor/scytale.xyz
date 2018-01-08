from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class MixedAlphabet(Cipher):
    name = "MixedAlphabet"

    def __init__(self, key=None, wildcard=None):
        self.key, self.wildcard = self.validate(key, wildcard=wildcard)

    def validate(self, key, wildcard=None):
        if key is None:
            key = "QWERTYUIOPASDFG_HJKLZXCVBNM"
        if len(key) != 27:
            raise ScytaleError("The Mixed Alphabet key must be 27 letters long; A-Z plus a space")
        key = key.upper()

        if wildcard is not None:
            if len(wildcard) != 1:
                raise ScytaleError("The Mixed Alphabet wildcard must be a single character")
            wildcard = wildcard.upper()
        else:
            if len(set(key)) != 27:
                raise ScytaleError("The Mixed Alphabet key must have 27 unique letters in it; A-Z plus a space")

        key = {self.alphabet[i]: k for i, k in enumerate(key)}

        return key, wildcard

    def substitute(self, char, key, wildcard=None):
        return key.get(char, wildcard)

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        return "".join(self.key.get(c, self.wildcard) for c in plaintext)

    def decrypt(self, ciphertext):
        key = {v: k for k, v in self.key.items()}
        return "".join(key.get(c, self.wildcard) for c in ciphertext)
