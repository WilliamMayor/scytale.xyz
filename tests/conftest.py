import pytest

from scytale import create_app
from scytale.models import db as app_db


@pytest.yield_fixture()
def app():
    a = create_app()
    ctx = a.app_context()
    ctx.push()
    yield a
    ctx.pop()


@pytest.yield_fixture()
def db(app):
    app_db.create_all()
    yield app_db
    app_db.session.rollback()
    app_db.drop_all()
