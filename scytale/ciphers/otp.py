from scytale.ciphers.base import Cipher


class OneTimePad(Cipher):
    name = "OneTimePad"

    def __init__(self, key=None):
        self.key = self.validate(key)

    def validate(self, key):
        if key is None:
            key = "IGBQU"
        key = key.upper()
        key = self.clean(key)
        return key

    def generate_pad(self, length):
        pad = self.key
        while len(pad) < length:
            pad += self.key
        return pad[:length]

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        pad = self.generate_pad(len(plaintext))
        a = self.alphabet
        return ''.join([
            a[(a.index(d) + a.index(p)) % len(a)]
            for d, p in zip(plaintext, pad)])

    def decrypt(self, ciphertext):
        pad = self.generate_pad(len(ciphertext))
        a = self.alphabet
        return ''.join([
            a[(a.index(d) - a.index(p)) % len(a)]
            for d, p in zip(ciphertext, pad)])
