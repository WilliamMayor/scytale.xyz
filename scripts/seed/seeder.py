import os

from scytale import create_app
from scytale.models import db, Group, Message


def create_admin():
    print("Creating admin group (Billy)")
    g = Group()
    g.name = "Billy"
    g.set_password(os.environ["ADMIN_PASSWORD"])
    return g


def create_message(group, cipher, key, plaintext, ciphertext):
    print("Creating message {} using {}".format(plaintext, cipher))
    m = Message()
    m.group = group
    m.cipher = cipher
    m.key = key
    m.plaintext = plaintext
    m.ciphertext = ciphertext
    return m


def create_messages(group):
    yield create_message(
        group, "Checkerboard", "RAIN OTS EQWYUPDFGHJKLZXCVBM .",
        "WELCOME TO VILLIERS PARK",
        "419818458798865888528181290788441080")
    yield create_message(
        group, "Checkerboard", "RAIN OTS EQWYUPDFGHJKLZXCVBM .",
        "I THINK YOU MEAN DRAUGHTS BOARD",
        "419818458798865888528181290788441080")

    yield create_message(
        group, "Mixed Alphabet", "QWERTYUIOPASDFG HJKLZXCVBNM",
        "WELCOME TO VILLIERS PARK",
        "CTSEGDTMLGMXOSSOTJKM QJA")
    yield create_message(
        group, "Mixed Alphabet", "QWERTYUIOPASDFG HJKLZXCVBNM",
        "BETTER THAN CAESAR",
        "WTLLTJMLIQFMEQTKQJ")

    yield create_message(
        group, "Playfair", "ILKENCRYPTOABDFGHMQSUVWXZ",
        "WELCOME TO VILLIERS PARK",
        "XKIRBGNPAULKKLLPQTHAEW")
    yield create_message(
        group, "Playfair", "ILKENCRYPTOABDFGHMQSUVWXZ",
        "YOU SHOULD ALWAYS PLAYFAIR",
        "CBZGGAVIFBKVBRQTRHTBOLPV")

    yield create_message(
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM",
        "WELCOME TO VILLIERS PARK",
        "QBZMUILSEOLXXQVTCZMMRCNY")
    yield create_message(
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM",
        "THE DAY OF THE TRIFIDS",
        "CHBVOGVWZYSPUPFXSMHMAY")

    yield create_message(
        group, "Fleissner",
        "XooXooooooXoXoooXoooXXoXoooooooooXoXoooXooooXoooXoXoooXXoooooooo",
        "WELCOME TO VILLIERS PARK",
        "WEXEXRXSXXL CXXXOPXXMEA XXXRXXXKXTXOXXX XXXXVXXXIXLXXXLIXXXXXXXX")
    yield create_message(
        group, "Fleissner",
        "XooXooooooXoXoooXoooXXoXoooooooooXoXoooXooooXoooXoXoooXXoooooooo",
        "FLEISSNER IS A FUNNY NAME",
        "FUXLXNXNXXEYIXXXS XXSNNEXXXAXXXMXRE XXXIXXXXSXXX XAXXX FXXXXXXXX")

    yield create_message(
        group, "Rail Fence", "5",
        "WELCOME TO VILLIERS PARK",
        "WTEE OIRKLE LSRCMVL AOIP")
    yield create_message(
        group, "Rail Fence", "5",
        "RAIL FENCE CIPHERS RULE",
        "RCRANEESIE H ELFCPRL IU")

    yield create_message(
        group, "Myszkowski", "VILLIERS",
        "WELCOME TO VILLIERS PARK",
        "MLAEOOIRPLC VS ELR IKWTE")
    yield create_message(
        group, "Myszkowski", "VILLIERS",
        "HOW DO YOU SPELL MYSZKOWSKI",
        "OEK ODUPMZK W  SYSI  LO YLW HO S")


if __name__ == '__main__':
    with create_app().app_context():
        a = create_admin()
        db.session.add(a)
        for m in create_messages(a):
            db.session.add(m)
            a.give_point(1, "Sent Message", max=5)
        db.session.commit()
