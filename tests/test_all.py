import pytest

from scytale.ciphers import Checkerboard, Fleissner, MixedAlphabet, Myszkowski, Permutation, OneTimePad, Playfair, RailFence, Shuffle, Trifid

params = (
    "Cipher",
    [Checkerboard, Fleissner, MixedAlphabet, Myszkowski, Permutation, OneTimePad, Playfair, RailFence, Shuffle, Trifid]
)


@pytest.mark.parametrize(*params)
def test_blank(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("")
    assert cipher.compare("", cipher.decrypt(ciphertext))


@pytest.mark.parametrize(*params)
def test_single_letter(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("a")
    print(ciphertext)
    assert cipher.compare("A", cipher.decrypt(ciphertext))


@pytest.mark.parametrize(*params)
def test_single_word(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("hello")
    assert cipher.compare("HELLO", cipher.decrypt(ciphertext))


@pytest.mark.parametrize(*params)
def test_sentence(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("how are you")
    assert cipher.compare("HOW ARE YOU", cipher.decrypt(ciphertext))


@pytest.mark.parametrize(*params)
def test_outside_alphabet(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("help!")
    assert cipher.compare("HELP", cipher.decrypt(ciphertext))


@pytest.mark.parametrize(*params)
def test_spaces_are_underscores(Cipher):
    cipher = Cipher()
    with_spaces = cipher.encrypt("how are you")
    with_underscores = cipher.encrypt("how_are_you")
    assert with_spaces == with_underscores


@pytest.mark.parametrize(*params)
def test_compare_spaces_and_underscores(Cipher):
    cipher = Cipher()
    assert cipher.compare("how are you", "how_are_you")
