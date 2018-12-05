import hashlib

from sqlalchemy.sql import func

from scytale.models import db


class Message(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    cipher = db.Column(db.Text)
    key = db.Column(db.Text)
    plaintext = db.Column(db.Text)
    ciphertext = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, server_default=func.now())

    group_id = db.Column(db.Integer, db.ForeignKey("group.gid"))
    group = db.relationship("Group", backref=db.backref("messages", lazy="dynamic"))

    @property
    def key_id(self):
        return hashlib.md5(self.key.encode()).hexdigest()
