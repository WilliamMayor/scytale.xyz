from scytale.ciphers import MixedAlphabet
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = MixedAlphabet()

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert "CTSEGDTMLGMXOSSOTJKM QJA" == ciphertext
    assert "WELCOME TO VILLIERS PARK" == cipher.decrypt(ciphertext)

    plaintext = cipher.decrypt("WTLLTJMLIQFMEQTKQJ")
    assert "BETTER THAN CAESAR" == plaintext
    assert "WTLLTJMLIQFMEQTKQJ" == cipher.encrypt(plaintext)


def test_key_too_short():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="abcd")


def test_key_too_long():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="abcdefghijklmnopqrstuvwxyz abc")


def test_key_has_repeating_chars():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="aacdefghijklmnopqrstuvwxyz ")
