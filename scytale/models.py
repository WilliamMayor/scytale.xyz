import string
import os

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    
    def check_password(self, candidate):
        return bcrypt.check_password_hash(self.password, candidate)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.uid)

    def __repr__(self):
        return '<User %r>' % (self.username)
