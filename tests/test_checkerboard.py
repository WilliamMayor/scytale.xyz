from scytale.ciphers import Checkerboard
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Checkerboard(key="RAIN OTS EQWYUPDFGHJKLZXCVBM_.")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare_ciphertext("419818458798865888528181290788441080", ciphertext)
    assert cipher.compare_plaintext("WELCOME TO VILLIERS PARK", cipher.decrypt(ciphertext))

    plaintext = cipher.decrypt("28864823808842543888791388450143474867888651045")
    assert cipher.compare_plaintext("I THINK YOU MEAN DRAUGHTS BOARD", plaintext)
    assert cipher.compare_ciphertext("28864823808842543888791388450143474867888651045", cipher.encrypt(plaintext))


def test_table_too_short():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiop")


def test_table_too_long():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiopasdfghjklzxcvbnmqwertyuiop")


def test_table_has_too_few_gaps():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rtyuiopasdfghjklzxcvbnm_.g")


def test_table_has_too_many_gaps():
    with pytest.raises(ScytaleError):
        Checkerboard(key="q we rty uiopasdfghjklzxcvbnm_")


def test_table_has_repeating_chars():
    with pytest.raises(ScytaleError):
        Checkerboard(key="qwe rty uiopqwertyuiopqwertyui")
