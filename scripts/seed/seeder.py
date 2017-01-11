import os

from scytale import create_app
from scytale.ciphers import MixedAlphabet
from scytale.models import db, Group, Message


def create_admin():
    print("Creating admin group (Billy)")
    g = Group()
    g.name = "Billy"
    g.set_password(os.environ["ADMIN_PASSWORD"])
    return g


def create_l33t_h4x0r():
    print("Creating leet group")
    g = Group()
    g.name = "L33t H4x0r"
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


def create_admin_messages(group):
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
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM ",
        "WELCOME TO VILLIERS PARK",
        "QBZMUILSEOLXXQVTCZMMRCNY ")
    yield create_message(
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM ",
        "THE DAY OF THE TRIFIDS",
        "CHBVOGVWZYSPUPFXSMHMAY ")

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

    yield create_message(
        group, "Permutation", "VILLIERS",
        "WELCOME TO VILLIERS PARK",
        "MEOLCE WLOI VLITARPS RKE")
    yield create_message(
        group, "Permutation", "VILLIERS",
        "ISNT THAT A HAIRSTYLE",
        "TS NTHAIA HA IRT TEYL  S")


def create_h4x0r_messages(group):

    # Short messages that can be brute forced
    messages = [
        "BLACK", "BLUE", "BROWN", "GREEN", "ORANGE", "PINK", "PURPLE", "RED",
        "WHITE", "YELLOW"
    ]
    cipher = MixedAlphabet(key="FNGZPOXKT HDLWEMQJRVCSYIBUA")
    for message in messages:
        yield create_message(
            group,
            "Mixed Alphabet",
            cipher.key,
            message,
            cipher.encrypt(message))

    # Long message that can be frequency analysed
    cipher = MixedAlphabet(key="IGLKWSREJDCANUFBZYP THMVXQO")
    message = "ALICE WAS BEGINNING TO GET VERY TIRED OF SITTING BY HER SISTER ON THE BANK AND OF HAVING NOTHING TO DO ONCE OR TWICE SHE HAD PEEPED INTO THE BOOK HER SISTER WAS READING BUT IT HAD NO PICTURES OR CONVERSATIONS IN IT AND WHAT IS THE USE OF A BOOK THOUGHT ALICE WITHOUT PICTURES OR CONVERSATION"
    yield create_message(
        group,
        "Mixed Alphabet",
        cipher.key,
        message,
        cipher.encrypt(message))

    # Messages that build on each other to construct the key
    messages = [
        "FIRST A LONG MESSAGE THAT HAS MOST LETTERS IN IT NOT ALL BUT MOST",
        "THEN A VERY SHORT MESSAGE",
        "FOLLOWED BY AN EXCEPTIONAL ONE"
    ]
    cipher = MixedAlphabet(key="AXT UWVCFGIMBOSNHZRYKEDJLPQ")
    for message in messages:
        yield create_message(
            group,
            "Mixed Alphabet",
            cipher.key,
            message,
            cipher.encrypt(message))


if __name__ == '__main__':
    with create_app().app_context():
        a = create_admin()
        db.session.add(a)
        for m in create_admin_messages(a):
            db.session.add(m)
            a.give_point(1, "Sent Message", max=5)

        h = create_l33t_h4x0r()
        db.session.add(h)
        for m in create_h4x0r_messages(h):
            db.session.add(m)
            h.give_point(1, "Sent Message", max=5)
        db.session.commit()
