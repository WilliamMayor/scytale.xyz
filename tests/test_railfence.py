from scytale.ciphers import RailFence
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = RailFence(key=5)

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("WTEE OIRKLE LSRCMVL AOIP", ciphertext), ciphertext
    plaintext = cipher.decrypt("WTEE OIRKLE LSRCMVL AOIP")
    assert cipher.compare("WELCOME TO VILLIERS PARK", plaintext), plaintext

    ciphertext = cipher.encrypt("RAIL FENCE CIPHERS RULE")
    assert cipher.compare("RCRANEESIE H ELFCPRL IU", ciphertext), ciphertext
    plaintext = cipher.decrypt("RCRANEESIE H ELFCPRL IU")
    assert cipher.compare("RAIL FENCE CIPHERS RULE", plaintext), plaintext


def test_key_not_integer():
    with pytest.raises(ScytaleError):
        RailFence(key="hello")


def test_hello_small():
    cipher = RailFence(key=2)
    assert "HLOEL" == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt("HLOEL")


def test_hello_smallish():
    cipher = RailFence(key=3)
    assert "HOELL" == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt("HOELL")
