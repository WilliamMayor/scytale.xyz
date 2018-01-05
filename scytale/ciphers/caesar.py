from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Caesar(Cipher):
    name = "Caesar"

    def __init__(self, key=13):
        self.key = self.validate(key)

    def validate(self, offset):
        if 0 >= offset > 27:
            raise ScytaleError("The Caesar key must be a number between 1 and 26")
        return offset

    def shift(self, text, offset):
        for c in text:
            i = self.alphabet.index(c)
            i = (i + offset) % len(self.alphabet)
            yield self.alphabet[i]

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        return "".join(self.shift(plaintext, self.key))

    def decrypt(self, ciphertext):
        return "".join(self.shift(ciphertext, -self.key))
