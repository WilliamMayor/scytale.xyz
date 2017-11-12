from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Myszkowski(Cipher):
    name = "Myszkowski"
    default = "VILLIERS"

    def __init__(self, key=None):
        self.key = self.validate(key)
        self.indexes = {}
        for i, c in enumerate(self.key):
            if c not in self.indexes:
                self.indexes[c] = []
            self.indexes[c].append(i)

    def validate(self, key):
        if key is None:
            key = self.default
        if len(key) < 2:
            raise ScytaleError("The Myszkowski key needs to be at least 2 letters")
        return key

    def compare(self, a, b):
        a = a.rstrip(" ")
        b = b.rstrip(" ")
        return super().compare(a, b)

    def pad(self, text):
        if len(text) % len(self.key) != 0:
            num_rows = len(text) // len(self.key) + 1
            text = text.ljust(len(self.key) * num_rows, "_")
        return text

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        plaintext = self.pad(plaintext)
        columns = [plaintext[i::len(self.key)] for i in range(len(self.key))]
        ciphertext = []
        for c in sorted(set(self.key)):
            indexes = self.indexes[c]
            for row in range(len(columns[0])):
                ciphertext.append("".join([columns[i][row] for i in indexes]))
        return "".join(ciphertext)

    def decrypt(self, ciphertext):
        columns = [None for _ in range(len(self.key))]
        depth = len(ciphertext) // len(self.key)
        for i, c in enumerate(sorted(set(self.key))):
            indexes = self.indexes[c]
            col_count = len(indexes)
            text, ciphertext = ciphertext[:depth * col_count], ciphertext[depth * col_count:]
            for j, k in enumerate(indexes):
                columns[k] = text[j::col_count]
        plaintext = []
        for row in range(depth):
            plaintext.append("".join([col[row] for col in columns]))
        return "".join(plaintext).rstrip(" ")
