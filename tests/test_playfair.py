from scytale.ciphers import Playfair
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Playfair(key="ILKENCRYPTOABDFGHMQSUVWXZ")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("XKIRBGNPAULKKLLPQTHAEW", ciphertext), ciphertext
    assert cipher.compare("WELCOME TO VILLIERS PARK", cipher.decrypt(ciphertext))

    assert cipher.compare("CBZGGAVIFBKVBRQTRHTBOLPV", cipher.encrypt("YOU SHOULD ALWAYS PLAYFAIR"))
    plaintext = cipher.decrypt("CBZGGAVIFBKVBRQTRHTBOLPV")
    assert cipher.compare("YOU SHOULD ALWAYS PLAYFAIR", plaintext)


def test_key_too_short():
    with pytest.raises(ScytaleError):
        Playfair(key="abcd")


def test_key_too_long():
    with pytest.raises(ScytaleError):
        Playfair(key="abcdefghijklmnopqrstuvwxyz")


def test_key_has_repeating_chars():
    with pytest.raises(ScytaleError):
        Playfair(key="aacdefghiklmnopqrstuvwxyz")


def test_next_two_simple():
    cipher = Playfair()
    text = ["A", "B"]
    assert ("A", "B") == cipher.next_two(text)
    assert [] == text


def test_next_two_same_letter():
    cipher = Playfair()
    text = ["A", "A", "B"]
    assert ("A", "X") == cipher.next_two(text)
    assert ["A", "B"] == text


def test_next_two_run_out():
    cipher = Playfair()
    text = ["A"]
    assert ("A", "X") == cipher.next_two(text)
    assert [] == text


def test_switch_square():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["G", "S"] == cipher.switch("I", "Q")


def test_switch_same_row():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["B", "D"] == cipher.switch("A", "C")


def test_switch_same_row_other_direction():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["A", "C"] == cipher.switch("B", "D", direction=-1)


def test_switch_same_row_wrap():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["A", "D"] == cipher.switch("E", "C")


def test_switch_same_column():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["L", "G"] == cipher.switch("G", "B")


def test_switch_same_column_other_direction():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["G", "B"] == cipher.switch("L", "G", direction=-1)


def test_switch_same_column_wrap():
    cipher = Playfair(key="abcdefghizklmnopqrstuvwxy")
    assert ["L", "B"] == cipher.switch("G", "V")
