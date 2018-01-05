import os

from scytale import create_app
from scytale.ciphers import MixedAlphabet, Playfair, Fleissner, Trifid, Myszkowski
from scytale.models import db, Group, Message
from scytale.forms import MessageForm


def create_group(name):
    print("Creating admin group ({})".format(name))
    group = Group()
    group.name = name
    group.set_password(os.environ["ADMIN_PASSWORD"])
    return group


def create_message(group, cipher, key, plaintext, ciphertext):
    print("Creating message:")
    print("    Group:", group.name)
    print("    Cipher:", cipher)
    print("    Key:", key)
    print("    Plaintext:", plaintext)
    print("    Ciphertext:", ciphertext)
    form = MessageForm(cipher=cipher, key=key, plaintext=plaintext, ciphertext=ciphertext, csrf_enabled=False)
    if form.validate():
        m = Message()
        m.group = group
        m.cipher = cipher
        m.key = key
        m.plaintext = plaintext
        m.ciphertext = ciphertext
        return m
    raise Exception('Invalid message: ' + str(form.errors))


def create_admin_messages(group):
    # yield create_message(
    #     group,"Checkerboard", "RAIN OTS EQWYUPDFGHJKLZXCVBM_.",
    #     "WELCOME TO VILLIERS PARK",
    #     "419818458798865888528181290788441080")
    # yield create_message(
    #     group, "Checkerboard", "RAIN OTS EQWYUPDFGHJKLZXCVBM_.",
    #     "I THINK YOU MEAN DRAUGHTS BOARD",
    #     "419818458798865888528181290788441080")

    # yield create_message(
    #     group, "Mixed Alphabet", "QWERTYUIOPASDFG_HJKLZXCVBNM",
    #     "WELCOME TO VILLIERS PARK",
    #     "CTSEGDTMLGMXOSSOTJKM QJA")
    # yield create_message(
    #     group, "Mixed Alphabet", "QWERTYUIOPASDFG_HJKLZXCVBNM",
    #     "BETTER THAN CAESAR",
    #     "WTLLTJMLIQFMEQTKQJ")

    yield create_message(
        group, "Playfair", "ILKENCRYPTOABDFGHMQSUVWXZ",
        "WELCOME TO VILLIERS PARK",
        "XKIRBGNPAULKKLLPQTHAEW")
    yield create_message(
        group, "Playfair", "ILKENCRYPTOABDFGHMQSUVWXZ",
        "YOU SHOULD ALWAYS PLAYFAIR",
        "CBZGGAVIFBKVBRQTRHTBOLPV")

    yield create_message(
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM_",
        "WELCOME TO VILLIERS PARK",
        "QBZMUILSEOLXXQVTCZMMRCNY")
    yield create_message(
        group, "Trifid", "QWERTYUIOPASDFGHJKLZXCVBNM_",
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

    # yield create_message(
    #     group, "Rail Fence", "5",
    #     "WELCOME TO VILLIERS PARK",
    #     "WTEE OIRKLE LSRCMVL AOIP")
    # yield create_message(
    #     group, "Rail Fence", "5",
    #     "RAIL FENCE CIPHERS RULE",
    #     "RCRANEESIE H ELFCPRL IU")

    yield create_message(
        group, "Myszkowski", "VILLIERS",
        "WELCOME TO VILLIERS PARK",
        "MLAEOOIRPLC VS ELR IKWTE")
    yield create_message(
        group, "Myszkowski", "VILLIERS",
        "HOW DO YOU SPELL MYSZKOWSKI",
        "OEK ODUPMZK W  SYSI  LO YLW HO S")

    # yield create_message(
    #     group, "Permutation", "VILLIERS",
    #     "WELCOME TO VILLIERS PARK",
    #     "MEOLCE WLOI VLITARPS RKE")
    # yield create_message(
    #     group, "Permutation", "VILLIERS",
    #     "ISNT THAT A HAIRSTYLE",
    #     "TS NTHAIA HA IRT TEYL  S")


def create_h4x0r_messages(group):

    # Short messages that can be brute forced
    messages = [
        "BLACK", "BLUE", "BROWN", "GREEN", "ORANGE", "PINK", "PURPLE", "RED",
        "WHITE", "YELLOW"
    ]
    cipher = MixedAlphabet(key="FNGZPOXKT_HDLWEMQJRVCSYIBUA")
    for message in messages:
        yield create_message(
            group,
            "Mixed Alphabet",
            cipher.key,
            message,
            cipher.encrypt(message))

    # Long message that can be frequency analysed
    cipher = MixedAlphabet(key="IGLKWSREJDCANUFBZYP_THMVXQO")
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


def create_activity_messages(group, ciphers, trifid, messages):

    for c, pt in zip(ciphers * 2, messages):
        yield create_message(
            group,
            cipher=c.name,
            key=c.key,
            plaintext=pt,
            ciphertext=c.encrypt(pt))

    pt = 'The {} key is {}'.format(ciphers[1].name, ciphers[1].key)
    yield create_message(
        group,
        cipher=ciphers[0].name,
        key=ciphers[0].key,
        plaintext=pt,
        ciphertext=ciphers[0].encrypt(pt))

    pt = 'The {} key is {}'.format(ciphers[2].name, ciphers[2].key)
    yield create_message(
        group,
        cipher=ciphers[1].name,
        key=ciphers[1].key,
        plaintext=pt,
        ciphertext=ciphers[1].encrypt(pt))

    pt = 'Line one of the Trifid key is {}'.format(trifid.key[0:9])
    yield create_message(
        group,
        cipher=ciphers[0].name,
        key=ciphers[0].key,
        plaintext=pt,
        ciphertext=ciphers[0].encrypt(pt))

    pt = 'Line two of the Trifid key is {}'.format(trifid.key[9:18])
    yield create_message(
        group,
        cipher=ciphers[1].name,
        key=ciphers[1].key,
        plaintext=pt,
        ciphertext=ciphers[1].encrypt(pt))

    pt = 'Line three of the Trifid key is {}'.format(trifid.key[18:27])
    yield create_message(
        group,
        cipher=ciphers[2].name,
        key=ciphers[2].key,
        plaintext=pt,
        ciphertext=ciphers[2].encrypt(pt))

    pt = 'CORRECT HORSE BATTERY STAPLE'
    # Don't return this one, don't want it on the site, where known plaintext could be used.
    create_message(
        group,
        cipher='Trifid',
        key=trifid.key,
        plaintext=pt,
        ciphertext=trifid.encrypt(pt))


def create_babbage_messages(group):
    playfair = Playfair(key='SCQOGUERPBKVWYZFDAHIMTLNX')
    myszkowski = Myszkowski(key='ENGINE')
    fleissner = Fleissner(key='ooooooXoooooXooXooooooooXoXoXoXoooooooooXXXoXooXooXoooXoXoooXooo')
    trifid = Trifid(key='HFERKDGNOQVJTMYP_AXSUBZWLIC')

    messages = [
        'CHARLES BABBAGE WAS BORN IN THE YEAR SEVENTEEN HUNDRED AND NINETY ONE',
        'BABBAGE INVENTED THE IDEA OF A DIGITAL PROGRAMMABLE COMPUTER',
        'CB IS CONSIDERED TO BE ONE OF THE FATHERS OF THE COMPUTER',
        'HIS MOST FAMOUS INVENTION IS THE DIFFERENCE ENGINE',
        'ON THE ECONOMY OF MACHINERY AND MANUFACTURES',
        'BABBAGE CRACKED THE UNCRACKABLE VIGENERE CIPHER',
    ]
    yield from create_activity_messages(group, [playfair, myszkowski, fleissner], trifid, messages)


def create_friedman_messages(group):
    playfair = Playfair(key='ADUQYKOMRETGVFHNWLXZCIPBS')
    myszkowski = Myszkowski(key='INDIANA')
    fleissner = Fleissner(key='oooXooooXXoXXooXXXooooXooooooooooooXoXoXXoXoXooooooooooooooooooX')
    trifid = Trifid(key='V_WLNJDOGRMHIPXKYQSETBZUAFC')

    messages = [
        'AMERICAS FIRST FEMALE CRYPTANALYST',
        'FRIEDMAN WAS BORN IN EIGHTEEN NINETY TWO',
        'CRACKED CODES AT RIVERBANK DURING WORLD WAR ONE',
        'USED CRYPTANALYSIS TO STOP SMUGGLING AND BOOTLEGGING',
        'SHE WORKED FOR THE US NAVY THE TREASURY DEPARTMENT AND THE COAST GUARD',
        'THE SHAKESPEAREAN CIPHERS EXAMINED'
    ]
    yield from create_activity_messages(group, [myszkowski, fleissner, playfair], trifid, messages)


def create_driscoll_messages(group):
    playfair = Playfair(key='CTOEFMUHYISAWNGQRZXLDKBVP')
    myszkowski = Myszkowski(key='ILLINOIS')
    fleissner = Fleissner(key='oooooooXXoooXoooXoXooooXXooooXoXooooXXooooooooXoXXooXXoooooooooo')
    trifid = Trifid(key='VAMZWXKSYONFTDUCHIBERGPJL_Q')

    messages = [
        'AGNES MEYER DRISCOLL WAS BORN IN EIGHTEEN EIGHTY NINE',
        'SHE WAS ALSO KNOWN AS MADAME X',
        'SHE WAS WITHOUT PEER AS A CRYPTANALYST',
        'DRISCOLL WORKED FOR THE US NAVY IN WORLD WAR ONE AND TWO',
        'SHE IS IN THE NATIONAL SECURITY AGENCYS HALL OF HONOR',
        'AGNES CRACKED JAPANESE NAVAL CODES INCLUDING THE RED AND BLUE BOOK CODES'
    ]
    yield from create_activity_messages(group, [fleissner, playfair, myszkowski], trifid, messages)


def create_tutte_messages(group):
    playfair = Playfair(key='KQSGLRYTWEUXBFPVDHMNZOCAI')
    myszkowski = Myszkowski(key='TUNNY')
    fleissner = Fleissner(key='oXXXooXXooXoXXooooooXooooooXoooooXooooooooooXXoXoXoooooooooXoooo')
    trifid = Trifid(key='_AWCDPYSEKQORNHBTLGJMVFIZXU')

    messages = [
        'WILLIAM THOMAS TUTTE WORKED AT BLETCHLEY PARK CRACKING GERMAN CIPHERS',
        'BILL WAS BORN IN SUFFOLK IN NINETEEN SEVENTEEN',
        'TUTTE WAS INSTRUMENTAL IN BREAKING THE GERMAN LORENZ CIPHER',
        'AN ALGEBRAIC THEORY OF GRAPHS',
        'TUTTE PERFORMED ONE OF THE GREATEST INTELLECTUAL FEATS OF WORLD WAR TWO',
        'UNLIKE IN THE MOVIE TUTTE DID NOT WORK DIRECTLY WITH TURING'
    ]
    yield from create_activity_messages(group, [myszkowski, fleissner, playfair], trifid, messages)


def create_rivest_messages(group):
    playfair = Playfair(key='PCGDAVESFOHMUWZLYNBRXKIQT')
    myszkowski = Myszkowski(key='CLIFFORD')
    fleissner = Fleissner(key='oXXXooXoooXoXoooXooooXooXooooXXooooXoooooooXooXoooooooXooooooooX')
    trifid = Trifid(key='AOGMPWEDZRCIBH_XTLVUQSNKYJF')

    messages = [
        'RONALD LINN RIVEST WAS BORN IN NINETEEN FOURTY SEVEN',
        'RIVEST IS ONE OF THE INVENTORS OF THE RSA ALGORITHM',
        'RON ALSO AUTHORED MANY OTHER ENCRYPTION ALGORITMS',
        'RONALD WORKS AS A CRYPTOGRAPHER AND INSTITUTE PROFESSOR AT MIT',
        'RIVEST WAS GIVEN A TURING AWARD IN TWO THOUSAND AND TWO',
        'RSA IS ONE OF THE FIRST PRACTICAL PUBLIC KEY CIPHERS IT IS USED EVERYWHERE'
    ]
    yield from create_activity_messages(group, [playfair, myszkowski, fleissner], trifid, messages)


def create_diffie_messages(group):
    playfair = Playfair(key='LSCZGADKUORFXTHQNBEPYMWIV')
    myszkowski = Myszkowski(key='HELLMAN')
    fleissner = Fleissner(key='ooooooooooooXoooXoooXoXXXoooXXXoooooooooooXooooooXXooooXooooXoXX')
    trifid = Trifid(key='CSQY_UBNVDWKPGERLTZJOHFAXMI')

    messages = [
        'BAILEY WHITFIELD DIFFIE WAS BORN IN NINETEEN FOURTY FOUR',
        'WHIT WAS THE COCREATOR OF DIFFIE HELLMAN KEY EXCHANGE',
        'DIFFIE GRADUATED FROM MIT IN NINETEEN SIXTY FIVE',
        'WITHOUT BAILEYS WORK THE INTERNET WOULD NOT BE POSSIBLE',
        'NEW DIRECTIONS IN CRYPTOGRAPHY',
        'HE HELPED DEVELOP THE FUNDAMENTAL IDEAS BEHIND PUBLIC KEY CIPHERS'
    ]
    yield from create_activity_messages(group, [fleissner, myszkowski, playfair], trifid, messages)


if __name__ == '__main__':
    with create_app().app_context():
        a = create_group("Billy")
        db.session.add(a)
        for m in create_admin_messages(a):
            db.session.add(m)
            a.give_point(1, "Sent Message", max=5)

        h = create_group("L33t H4x0r")
        db.session.add(h)
        for m in create_h4x0r_messages(h):
            db.session.add(m)
            h.give_point(1, "Sent Message", max=5)

        g = create_group("Babbage")
        for m in create_babbage_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        g = create_group("Friedman")
        for m in create_friedman_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        g = create_group("Driscoll")
        for m in create_driscoll_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        g = create_group("Tutte")
        for m in create_tutte_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        g = create_group("Rivest")
        for m in create_rivest_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        g = create_group("Diffie")
        for m in create_diffie_messages(g):
            g.give_point(1, "Sent Message", max=5)
            db.session.add(m)

        db.session.commit()
