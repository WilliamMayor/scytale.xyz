from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Permutation(Cipher):
    default = "VILLIERS"

    def __init__(self, key=None, alphabet=None):
        self.alphabet = alphabet or Cipher.alphabet
        self.key = self.validate_key(key)

        self.indexes = {}
        for i, c in enumerate(self.key):
            if c not in self.indexes:
                self.indexes[c] = []
            self.indexes[c].append(i)

    def validate_key(self, key):
        if key is None:
            key = self.default
        if len(key) < 2:
            raise ScytaleError("The Permutation key needs to be at least 2 letters")
        return key

    def compare(self, a, b):
        a = a.rstrip(" ")
        b = b.rstrip(" ")
        return super().compare(a, b)

    def pad(self, text):
        padding = len(text) % len(self.key)
        if padding > 0:
            return text + " " * (len(self.key) - padding)
        return text

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        plaintext = self.pad(plaintext)
        columns = [
            (k, plaintext[i::len(self.key)])
            for i, k in enumerate(self.key)]
        columns = sorted(columns, key=lambda c: c[0])
        columns = [c[1] for c in columns]
        return "".join("".join(r) for r in zip(*columns))

    def decrypt(self, ciphertext):
        columns = [
            (k, ciphertext[i::len(self.key)])
            for i, k in enumerate(sorted(self.key))]
        key = list(self.key)

        def key_func(col):
            i = key.index(col[0])
            key[i] = None
            return i
        columns = sorted(columns, key=key_func)
        columns = [c[1] for c in columns]
        return "".join("".join(r) for r in zip(*columns))
