from scytale.ciphers.base import Cipher
from scytale.exceptions import ScytaleError


class Checkerboard(Cipher):
    name = "Checkerboard"
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_."

    def __init__(self, key=None):
        self.table = self.validate(key)
        self.blanks = self.find_blanks(self.table)
        self.init_char_to_numbers(key)
        self.init_number_to_chars(key)

    def validate(self, table):
        if table is None:
            table = "RAIN OTS EQWYUPDFGHJKLZXCVBM_."
        table = table.upper()
        if len(table) != 30:
            raise ScytaleError("Checkerboard table needs to be 30 characters long")
        rows = [table[0:10], table[10:20], table[20:30]]
        if list(rows[0]).count(" ") != 2:
            raise ScytaleError(
                "The first row in the Checkerboard table must have 2 spaces"
            )
        if len(set(table)) != 29:  # Extra one for gaps in top row
            raise ScytaleError(
                "The Checkerboard table must have 28 unique letters in it"
            )
        return rows

    def find_blanks(self, table):
        blanks = []
        for i, c in enumerate(table[0]):
            if c == " ":
                blanks.append(i)
        return blanks

    def init_char_to_numbers(self, table):
        self.char_to_numbers = {}
        for i, c in enumerate(self.table[0]):
            if c != " ":
                self.char_to_numbers[c] = (i,)
        for i, c in enumerate(self.table[1]):
            self.char_to_numbers[c] = (self.blanks[0], i)
        for i, c in enumerate(self.table[2]):
            self.char_to_numbers[c] = (self.blanks[1], i)

    def init_number_to_chars(self, table):
        self.number_to_chars = {}
        for i, c in enumerate(self.table[0]):
            if c != " ":
                self.number_to_chars[i] = c
            else:
                self.number_to_chars[i] = {}
        for i, c in enumerate(self.table[1]):
            self.number_to_chars[self.blanks[0]][i] = c
        for i, c in enumerate(self.table[2]):
            self.number_to_chars[self.blanks[1]][i] = c

    def encrypt(self, plaintext):
        plaintext = self.clean(plaintext.upper())
        return "".join(
            [str(number) for c in plaintext for number in self.char_to_numbers[c]]
        )

    def decrypt(self, ciphertext):
        plaintext = []
        numbers = list(ciphertext)
        while numbers:
            index = int(numbers.pop(0))
            c = self.number_to_chars[index]
            if isinstance(c, str):
                plaintext.append(c)
            else:
                index = int(numbers.pop(0))
                plaintext.append(c[index])
        return "".join(plaintext)
