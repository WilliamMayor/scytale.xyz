from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Playfair(Cipher):
    default = "ILKENCRYPTOABDFGHMQSUVWXZ"

    def __init__(self, key=None):
        self.key = self.validate(key)

    def compare(self, a, b):
        a = a.replace("J", "I").replace(" ", "").replace("X", "")
        b = b.replace("J", "I").replace(" ", "").replace("X", "")
        return super().compare(a, b)

    def validate(self, key):
        if key is None:
            key = self.default
        if len(key) != 25:
            raise ScytaleError("The Playfair key must be 25 letters long; a 5x5 grid")
        key = key.upper()
        for l in self.default:
            if l not in key:
                raise ScytaleError("Missing letter in key: {0}".format(l))
        return key

    def switch(self, one, two, direction=1):
        one_index = self.key.index(one)
        two_index = self.key.index(two)
        one_row = one_index // 5
        one_column = one_index % 5
        two_row = two_index // 5
        two_column = two_index % 5
        if one_row == two_row:
            one_column = (one_column + direction) % 5
            two_column = (two_column + direction) % 5
        elif one_column == two_column:
            one_row = (one_row + direction) % 5
            two_row = (two_row + direction) % 5
        else:
            one_column, two_column = two_column, one_column
        return [
            self.key[one_row * 5 + one_column],
            self.key[two_row * 5 + two_column]
        ]

    def next_two(self, remaining):
        one = remaining.pop(0)
        if not remaining or remaining[0] == one:
            two = "X"
        else:
            two = remaining.pop(0)
        return one, two

    def process(self, text_in, direction=1):
        text_in = list(text_in)
        text_out = []
        while text_in:
            one, two = self.next_two(text_in)
            text_out += self.switch(one, two, direction=direction)
        return "".join(text_out)

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        plaintext = plaintext.replace("J", "I").replace(" ", "")
        return self.process(plaintext)

    def decrypt(self, ciphertext):
        return self.process(ciphertext, direction=-1)

    def hack(self, ciphertext):
        raise NotImplementedError("Cannot hack Playfair in any reasonable time")
