from scytale.ciphers import Myszkowski
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Myszkowski(key="VILLIERS")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("MLAEOOIRPLC VS ELR IKWTE", ciphertext), ciphertext
    plaintext = cipher.decrypt("MLAEOOIRPLC VS ELR IKWTE")
    assert cipher.compare("WELCOME TO VILLIERS PARK", plaintext), plaintext

    ciphertext = cipher.encrypt("HOW DO YOU SPELL MYSZKOWSKI")
    assert cipher.compare("OEK ODUPMZK W  SYSI  LO YLW HO S", ciphertext), ciphertext
    plaintext = cipher.decrypt("OEK ODUPMZK W  SYSI  LO YLW HO S")
    assert cipher.compare("HOW DO YOU SPELL MYSZKOWSKI", plaintext), plaintext


def test_key_blank():
    with pytest.raises(ScytaleError):
        Myszkowski(key="")


def test_key_too_small():
    with pytest.raises(ScytaleError):
        Myszkowski(key="A")


def test_compare():
    cipher = Myszkowski()
    assert cipher.compare("A", "A  ")


def test_pad():
    cipher = Myszkowski(key="ABC")
    assert "A  " == cipher.pad("A")


def test_pad_nothing_needed():
    cipher = Myszkowski(key="ABC")
    assert "AAA" == cipher.pad("AAA")


def test_pad_two_rows():
    cipher = Myszkowski(key="ABC")
    assert "AAAA  " == cipher.pad("AAAA")


def test_hello_with_hello():
    cipher = Myszkowski(key="HELLO")
    assert "EHLLO" == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt("EHLLO")


def test_hello():
    cipher = Myszkowski(key="VILLIERS")
    #                        HELLO
    assert " EOLL  H" == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt(" EOLL  H")


def test_hello_small_key():
    cipher = Myszkowski(key="HI")
    #                        HELLO
    assert "HLOEL " == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt("HLOEL ")
