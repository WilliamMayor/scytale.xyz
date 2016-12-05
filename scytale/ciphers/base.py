

class Cipher:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def clean(self, text):
        return ''.join(filter(lambda c: c in self.alphabet, text))

    def compare(self, a, b):
        """Simple comparison function that can be overwritten when letters in
        the ciphertext should be ignored"""
        return a == b
