from scytale.ciphers import Shuffle


def test_from_cryptanalysis_presentation_phoenix():
    cipher = Shuffle([1, 9, 4, 5, 8, 2, 0, 6, 13, 7, 10, 11, 12, 3])

    ciphertext = cipher.encrypt("PHOENIX")
    assert ciphertext == "H_NI_OPX_____E"
    assert cipher.decrypt(ciphertext) == "PHOENIX"

    ciphertext = cipher.encrypt("ATTACK_AT_DAWN")
    assert ciphertext == "T_CKTTA_NADAWA"
    assert cipher.decrypt(ciphertext) == "ATTACK_AT_DAWN"

    ciphertext = cipher.encrypt("YES_IM_SURE")
    assert ciphertext == "ERIMUSY__SE___"
    assert cipher.decrypt(ciphertext) == "YES_IM_SURE"


def test_from_cryptanalysis_presentation_wolverine():
    cipher = Shuffle([9, 4, 12, 11, 15, 5, 8, 7, 13, 0, 14, 3, 16, 2, 6, 1, 10])

    ciphertext = cipher.encrypt("WOLVERINE")
    assert ciphertext == "_E___REN_W_V_LIO_"
    assert cipher.decrypt(ciphertext) == "WOLVERINE"

    ciphertext = cipher.encrypt("DAWN_ARE_YOU_SURE")
    assert ciphertext == "Y__URA_ESDUNEWRAO"
    assert cipher.decrypt(ciphertext) == "DAWN_ARE_YOU_SURE"

    ciphertext = cipher.encrypt("ROGER_THAT")
    assert ciphertext == "TR____AH_R_E_GTO_"
    assert cipher.decrypt(ciphertext) == "ROGER_THAT"
