

class Cipher:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def clean(self, text):
        return ''.join(filter(lambda c: c in self.alphabet, text))

    def compare(self, a, b):
        return a == b
