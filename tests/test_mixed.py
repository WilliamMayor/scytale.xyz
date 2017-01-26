from scytale.ciphers import MixedAlphabet
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = MixedAlphabet(key="QWERTYUIOPASDFG HJKLZXCVBNM")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare_ciphertext("CTSEGDTMLGMXOSSOTJKM QJA", ciphertext)
    assert cipher.compare_plaintext("WELCOME TO VILLIERS PARK", cipher.decrypt(ciphertext))

    plaintext = cipher.decrypt("WTLLTJMLIQFMEQTKQJ")
    assert cipher.compare_plaintext("BETTER THAN CAESAR", plaintext)
    assert cipher.compare_ciphertext("WTLLTJMLIQFMEQTKQJ", cipher.encrypt(plaintext))


def test_key_too_short():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="abcd")


def test_key_too_long():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="abcdefghijklmnopqrstuvwxyz abc")


def test_key_has_repeating_chars():
    with pytest.raises(ScytaleError):
        MixedAlphabet(key="aacdefghijklmnopqrstuvwxyz ")
