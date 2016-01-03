import pytest

from scytale.ciphers import Checkerboard, MixedAlphabet

params = (
    "Cipher",
    [Checkerboard, MixedAlphabet]
)


@pytest.mark.parametrize(*params)
def test_blank(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("")
    assert "" == cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_single_letter(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("a")
    print(ciphertext)
    assert "A" == cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_single_word(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("hello")
    assert "HELLO" == cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_sentence(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("how are you")
    assert "HOW ARE YOU" == cipher.decrypt(ciphertext)


@pytest.mark.parametrize(*params)
def test_outside_alphabet(Cipher):
    cipher = Cipher()
    ciphertext = cipher.encrypt("help!")
    assert "HELP" == cipher.decrypt(ciphertext)
