

class Cipher:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def clean(self, text):
        return ''.join(filter(lambda c: c in self.alphabet, text))
