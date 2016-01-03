from scytale.ciphers import Checkerboard
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Checkerboard(key="RAIN OTS EQWYUPDFGHJKLZXCVBM .")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert "419818458798865888528181290788441080" == ciphertext
    assert "WELCOME TO VILLIERS PARK" == cipher.decrypt(ciphertext)

    plaintext = cipher.decrypt("28864823808842543888791388450143474867888651045")
    assert "I THINK YOU MEAN DRAUGHTS BOARD" == plaintext
    assert "28864823808842543888791388450143474867888651045" == cipher.encrypt(plaintext)


def test_table_too_short():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiop")


def test_table_too_long():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiopasdfghjklzxcvbnmqwertyuiop")


def test_table_has_too_few_gaps():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rtyuiopasdfghjklzxcvbnm .g")


def test_table_has_too_many_gaps():
    with pytest.raises(ScytaleError):
        Checkerboard(key="q we rty uiopasdfghjklzxcvbnm ")


def test_table_has_repeating_chars():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiopqwertyuiopqwertyui")
