from scytale.ciphers import Fleissner
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Fleissner(key="XooXooooooXoXoooXoooXXoXoooooooooXoXoooXooooXoooXoXoooXXoooooooo")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("WEXEXRXSXXL CXXXOPXXMEA XXXRXXXKXTXOXXX XXXXVXXXIXLXXXLIXXXXXXXX", ciphertext), ciphertext
    plaintext = cipher.decrypt("WEXEXRXSXXL CXXXOPXXMEA XXXRXXXKXTXOXXX XXXXVXXXIXLXXXLIXXXXXXXX")
    assert cipher.compare("WELCOME TO VILLIERS PARK", plaintext), plaintext

    ciphertext = cipher.encrypt("FLEISSNER IS A FUNNY NAME")
    assert cipher.compare("FUXLXNXNXXEYIXXXS XXSNNEXXXAXXXMXRE XXXIXXXXSXXX XAXXX FXXXXXXXX", ciphertext), ciphertext
    plaintext = cipher.decrypt("FUXLXNXNXXEYIXXXS XXSNNEXXXAXXXMXRE XXXIXXXXSXXX XAXXX FXXXXXXXX")
    assert cipher.compare("FLEISSNER IS A FUNNY NAME", plaintext), plaintext


def test_key_not_square():
    with pytest.raises(ScytaleError):
        Fleissner(key="Xoo")


def test_key_contains_something_else():
    with pytest.raises(ScytaleError):
        Fleissner(key="ABC")


def test_key_has_overlapping_cuts():
    with pytest.raises(ScytaleError):
        Fleissner(key="XXoo")


def test_grille():
    cipher = Fleissner(key="XooooXoXoooooXoo")
    assert [
        ["X", "o", "o", "o"],
        ["o", "X", "o", "X"],
        ["o", "o", "o", "o"],
        ["o", "X", "o", "o"]] == cipher.grille


def test_rotate():
    cipher = Fleissner(key="XooooXoXoooooXoo")
    assert [
        ("o", "o", "o", "X"),
        ("X", "o", "X", "o"),
        ("o", "o", "o", "o"),
        ("o", "o", "X", "o")] == cipher.rotate(cipher.grille)


def test_rotate_back_again():
    cipher = Fleissner(key="XooooXoXoooooXoo")
    rotated = cipher.rotate(cipher.grille)
    assert [
        ("X", "o", "o", "o"),
        ("o", "X", "o", "X"),
        ("o", "o", "o", "o"),
        ("o", "X", "o", "o")] == cipher.rotate(rotated, clockwise=False)


def test_very_large_plaintext():
    cipher = Fleissner(key="XooooXoXoooooXoo")
    ciphertext = cipher.encrypt("A" * 32)
    assert len(ciphertext) == 32


def test_hello():
    cipher = Fleissner(key="XooooXoXoooooXoo")
    assert "HXXOXEXLXXXXXLXX" == cipher.encrypt("HELLO")
    assert "HELLO" == cipher.decrypt("HXXOXEXLXXXXXLXX")
