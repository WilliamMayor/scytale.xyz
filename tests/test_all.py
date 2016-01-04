import pytest

from scytale.ciphers import Checkerboard, Fleissner, MixedAlphabet, Playfair, Trifid

params = (
    "Cipher",
    [Checkerboard, Fleissner, MixedAlphabet, Playfair, Trifid]
)


@pytest.mark.parametrize(*params)
def test_blank(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("")
    assert cipher.compare("", cipher.decrypt(ciphertext)), cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_single_letter(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("a")
    print(ciphertext)
    assert cipher.compare("A", cipher.decrypt(ciphertext)), cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_single_word(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("hello")
    assert cipher.compare("HELLO", cipher.decrypt(ciphertext)), cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_sentence(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("how are you")
    assert cipher.compare("HOW ARE YOU", cipher.decrypt(ciphertext)), cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_outside_alphabet(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("help!")
    assert cipher.compare("HELP", cipher.decrypt(ciphertext)), cipher.decrypt(ciphertext)
