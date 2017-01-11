import math

from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Fleissner(Cipher):
    default = "XooXooooooXoXoooXoooXXoXoooooooooXoXoooXooooXoooXoXoooXXoooooooo"

    def __init__(self, key=None):
        self.key = self.validate(key)
        self.grille = self.init_grille(self.key)
        self.key_size = len(self.key)
        self.grille_size = len(self.grille)
        all_a = self.encrypt("A" * self.key_size)
        all_a = all_a.replace("X", "")
        if len(all_a) != self.key_size:
            raise ScytaleError("Either a space in the grille overlaps another, or your gaps do not cover the grid.")

    def compare_ciphertext(self, actual, candidate):
        """Returns true if the two ciphertexts are equivalent in this cipher"""
        actual = self.make_comparable(self.decrypt(actual))
        candidate = self.make_comparable(self.decrypt(candidate))
        return candidate.startswith(actual)  # i.e. ignore any final random letters

    def validate(self, key):
        if key is None:
            key = self.default
        xo = set(list(key))
        if xo != set(["X", "o"]):
            raise ScytaleError("The Fleissner Grille key must be a string of X (cut) and o (don't cut) letters only")
        length = len(key)
        sqrt = int(math.sqrt(length))
        if math.pow(sqrt, 2) != length:
            raise ScytaleError("You cannot form a square from {0} cells".format(length))
        return key

    def init_grille(self, key):
        size = int(math.sqrt(len(key)))
        return [list(key[i:i + size]) for i in range(0, len(key), size)]

    def rotate(self, grille, clockwise=True):
        if clockwise:
            return list(zip(*grille[::-1]))
        return list(zip(*grille))[::-1]

    def next_cell(self, grille, row, column):
        if column == self.grille_size - 1:
            column = 0
            if row == self.grille_size - 1:
                row = 0
                grille = self.rotate(grille)
            else:
                row += 1
        else:
            column += 1
        return grille, row, column

    def space_at(self, grille, row=0, column=0):
        space = grille[row][column]
        while space != "X":
            grille, row, column = self.next_cell(grille, row, column)
            space = grille[row][column]
        return grille, row, column

    def write(self, text):
        ciphertext = ["X" for _ in range(self.key_size)]
        row, column = 0, 0
        grille = self.grille
        while text:
            grille, row, column = self.space_at(grille, row=row, column=column)
            ciphertext[self.grille_size * row + column] = text.pop(0)
            grille, row, column = self.next_cell(grille, row, column)
        return "".join(ciphertext)

    def read(self, text):
        plaintext = []
        row, column = 0, 0
        grille = self.grille
        for _ in range(self.key_size):
            grille, row, column = self.space_at(grille, row=row, column=column)
            plaintext.append(text[self.grille_size * row + column])
            grille, row, column = self.next_cell(grille, row, column)
        return "".join(plaintext)

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        texts = [
            list(plaintext[i:i + self.key_size])
            for i in range(0, len(plaintext), self.key_size)]
        return "".join([self.write(t) for t in texts])

    def decrypt(self, ciphertext):
        texts = [
            list(ciphertext[i:i + self.key_size])
            for i in range(0, len(ciphertext), self.key_size)]
        plaintext = "".join([self.read(t) for t in texts])
        return plaintext.rstrip("X")
