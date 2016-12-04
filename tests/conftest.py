import pytest

from scytale import create_app


@pytest.yield_fixture()
def app():
    a = create_app()
    ctx = a.app_context()
    ctx.push()
    yield a
    ctx.pop()
