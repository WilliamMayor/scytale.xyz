import os

from flask import Flask

from scytale.views import bp
from scytale import jinja, login, models


def boolify(s):
    if s.lower() == 'true':
        return True
    if s.lower() == 'false':
        return False
    raise ValueError("%s is not one of 'True' or 'False'" % s)


def auto_convert(s):
    for fn in (boolify, int, float):
        try:
            return fn(s)
        except ValueError:
            pass
    return s


def create_app():
    app = Flask(__name__)

    app.config.from_object('scytale.config')
    app.config.update({
        k: auto_convert(os.environ[k])
        for k in app.config
        if k in os.environ})

    jinja.init_app(app)
    login.init_app(app)
    models.init_app(app)

    app.register_blueprint(bp)
    return app
