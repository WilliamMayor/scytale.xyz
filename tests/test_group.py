from scytale.models import Group


def test_passwords(db):
    g = Group()
    g.set_password("hunter2")
    assert g.check_password("hunter2")
    assert not g.check_password("password123")


def test_password_from_db(db):
    g = Group()
    g.name = "ByteStrings!"
    g.set_password("hunter2")
    db.session.add(g)
    db.session.commit()
    assert g.check_password("hunter2")
    assert not g.check_password("password123")
