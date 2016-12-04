from scytale.models import Group


def test_passwords():
    g = Group()
    g.set_password("hunter2")
    assert g.check_password("hunter2")
    assert not g.check_password("password123")
