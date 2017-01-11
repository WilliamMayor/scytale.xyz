from scytale.exceptions import ScytaleError


class Cipher:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def clean(self, text):
        return ''.join(filter(lambda c: c in self.alphabet, text))

    def make_comparable(self, text):
        return text.upper().replace("_", " ")

    def compare(self, a, b):
        """Simple comparison function that can be overwritten when letters in
        the ciphertext should be ignored"""
        return self.make_comparable(a) == self.make_comparable(b)

    def compare_plaintext(self, a, b):
        """Returns true if the two plaintexts are equivalent in this cipher"""
        return self.compare(a, b)

    def compare_ciphertext(self, a, b):
        """Returns true if the two ciphertexts are equivalent in this cipher"""
        return self.compare(a, b)

    def validate_plaintext(self, plaintext):
        if not all(p in self.alphabet for p in plaintext):
            raise ScytaleError("Some plaintext letters are not in your alphabet")
