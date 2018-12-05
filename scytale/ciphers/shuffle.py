import random

from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Shuffle(Cipher):
    name = "Shuffle"
    """Only used in the known-plaintext attack slide"""

    def __init__(self, key=None):
        self.key = self.validate(key)

    def validate(self, indexes):
        if indexes is None:
            indexes = list(range(0, 14))
            random.shuffle(indexes)
        if len(set(indexes)) != len(indexes):
            raise ScytaleError(
                "The shuffle cipher must not have repeating numbers in its key"
            )
        return indexes

    def pad(self, text):
        if len(text) == 0:
            text = "_" * len(self.key)
        if len(text) % len(self.key) != 0:
            num_rows = len(text) // len(self.key) + 1
            text = text.ljust(len(self.key) * num_rows, "_")
        return text

    def encrypt(self, plaintext):
        if len(plaintext) > len(self.key):
            raise ScytaleError("Plaintext too big")
        plaintext = self.clean(plaintext.upper())
        plaintext = self.pad(plaintext)
        return "".join(plaintext[i] for i in self.key)

    def decrypt(self, ciphertext):
        return "".join(
            ciphertext[c] for c, p in sorted(enumerate(self.key), key=lambda k: k[1])
        ).rstrip(
            "_"
        )
