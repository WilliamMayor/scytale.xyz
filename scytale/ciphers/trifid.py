from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Trifid(Cipher):
    default = "QWERTYUIOPASDFGHJKLZXCVBNM "

    def __init__(self, key=None):
        self.key = self.validate(key)
        self.cton = self.init_cton(self.key)
        self.ntoc = {v: k for k, v in self.cton.items()}

    def validate(self, key):
        if key is None:
            key = self.default
        if len(key) != 27:
            raise ScytaleError("The Trifid key must be 27 letters long; a 3x3x3 grid")
        key = key.upper()
        for l in self.default:
            if l not in key:
                raise ScytaleError("Missing letter in key: {0}".format(l))
        return key

    def init_cton(self, key):
        cton = {}
        for i, c in enumerate(key):
            box = (i % 9) // 3
            row = i // 9
            column = i % 3
            cton[c] = "{box}{row}{column}".format(box=box, row=row, column=column)
        return cton

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        ciphertext = []
        coords = [self.cton[c] for c in plaintext]
        coords = [n[i] for i in range(3) for n in coords]
        while coords:
            coord, coords = "".join(coords[0:3]), coords[3:]
            ciphertext.append(self.ntoc[coord])
        return "".join(ciphertext)

    def decrypt(self, ciphertext):
        length = len(ciphertext)
        coords = "".join([self.cton[c] for c in ciphertext])
        coords = [coords[i::length] for i in range(length)]
        return "".join([self.ntoc[n] for n in coords])

    def hack(self, ciphertext):
        raise NotImplementedError("Cannot hack mixed alphabet in any reasonable time")
