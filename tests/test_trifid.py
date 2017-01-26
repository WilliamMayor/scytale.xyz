from scytale.ciphers import Trifid
from scytale.exceptions import ScytaleError

import pytest


def test_from_worksheet():
    cipher = Trifid(key="QWERTYUIOPASDFGHJKLZXCVBNM ")

    ciphertext = cipher.encrypt("WELCOME TO VILLIERS PARK")
    assert cipher.compare("QBZMUILSEOLXXQVTCZMMRCNY", ciphertext), ciphertext
    assert cipher.compare("WELCOME TO VILLIERS PARK", cipher.decrypt(ciphertext))

    ciphertext = cipher.encrypt("THE DAY OF THE TRIFIDS")
    assert cipher.compare("CHBVOGVWZYSPUPFXSMHMAY", ciphertext), ciphertext
    plaintext = cipher.decrypt("CHBVOGVWZYSPUPFXSMHMAY")
    assert cipher.compare("THE DAY OF THE TRIFIDS", plaintext), plaintext


def test_key_too_short():
    with pytest.raises(ScytaleError):
        Trifid(key="abcd")


def test_key_too_long():
    with pytest.raises(ScytaleError):
        Trifid(key="abcdefghijklmnopqrstuvwxyz_.")


def test_key_has_repeating_chars():
    with pytest.raises(ScytaleError):
        Trifid(key="aacdefghiklmnopqrstuvwxyz_")


def test_cton():
    cipher = Trifid(key="QWERTYUIOPASDFGHJKLZXCVBNM_")
    cton = cipher.cton
    assert cton["Q"] == "000"
    assert cton["W"] == "001"
    assert cton["E"] == "002"
    assert cton["R"] == "100"
    assert cton["T"] == "101"
    assert cton["Y"] == "102"
    assert cton["U"] == "200"
    assert cton["I"] == "201"
    assert cton["O"] == "202"
    assert cton["P"] == "010"
    assert cton["A"] == "011"
    assert cton["S"] == "012"
    assert cton["D"] == "110"
    assert cton["F"] == "111"
    assert cton["G"] == "112"
    assert cton["H"] == "210"
    assert cton["J"] == "211"
    assert cton["K"] == "212"
    assert cton["L"] == "020"
    assert cton["Z"] == "021"
    assert cton["X"] == "022"
    assert cton["C"] == "120"
    assert cton["V"] == "121"
    assert cton["B"] == "122"
    assert cton["N"] == "220"
    assert cton["M"] == "221"
    assert cton["_"] == "222"
