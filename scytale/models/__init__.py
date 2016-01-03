from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    bcrypt.init_app(app)
    db.init_app(app)

from scytale.models.point import Point
from scytale.models.group import Group
from scytale.models.message import Message
__all__ = [
    db,
    bcrypt,
    Group,
    Message,
    Point
]
