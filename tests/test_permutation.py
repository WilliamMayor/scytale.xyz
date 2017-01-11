from scytale.ciphers import Permutation
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Permutation(key="VILLIERS")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("MEOLCE WLOI VLITARPS RKE", ciphertext), ciphertext
    plaintext = cipher.decrypt("MEOLCE WLOI VLITARPS RKE")
    assert cipher.compare("WELCOME TO VILLIERS PARK", plaintext), plaintext

    ciphertext = cipher.encrypt("ISNT THAT A HAIRSTYLE")
    assert cipher.compare("TS NTHAIA HA IRT TEYL  S", ciphertext), ciphertext
    plaintext = cipher.decrypt("TS NTHAIA HA IRT TEYL  S")
    assert cipher.compare("ISNT THAT A HAIRSTYLE", plaintext), plaintext


def test_from_website():
    # http://crypto.interactive-maths.com/permutation-cipher.html
    cipher = Permutation(key="BAD")

    ciphertext = cipher.encrypt("THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG")
    assert cipher.compare("HTEUQIKCBORWFNOJXUPMEODVRETEHLZAYODG", ciphertext), ciphertext

    plaintext = cipher.decrypt("HTEUQIKCBORWFNOJXUPMEODVRETEHLZAYODG")
    assert cipher.compare("THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG", plaintext), plaintext


def test_key_blank():
    with pytest.raises(ScytaleError):
        Permutation(key="")


def test_key_too_small():
    with pytest.raises(ScytaleError):
        Permutation(key="A")


def test_compare():
    cipher = Permutation()
    assert cipher.compare("A", "A  ")


def test_pad():
    cipher = Permutation(key="ABC")
    assert "A  " == cipher.pad("A")


def test_pad_nothing_needed():
    cipher = Permutation(key="ABC")
    assert "AAA" == cipher.pad("AAA")


def test_pad_two_rows():
    cipher = Permutation(key="ABC")
    assert "AAAA  " == cipher.pad("AAAA")
