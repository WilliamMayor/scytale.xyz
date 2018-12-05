from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class RailFence(Cipher):
    name = "RailFence"
    default = 5

    def __init__(self, key=None):
        self.key = self.validate(key)

    def validate(self, key):
        if key is None:
            key = self.default
        try:
            return int(key)
        except:
            raise ScytaleError("The Rail Fence key should be a number")

    def fence(self, text):
        fence = [[None] * len(text) for n in range(self.key)]
        rails = list(range(self.key - 1)) + list(range(self.key - 1, 0, -1))
        for n, x in enumerate(text):
            fence[rails[n % len(rails)]][n] = x
        return [c for rail in fence for c in rail if c is not None]

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        return "".join(self.fence(plaintext))

    def decrypt(self, ciphertext):
        rng = range(len(ciphertext))
        pos = self.fence(rng)
        return "".join(ciphertext[pos.index(n)] for n in rng)
