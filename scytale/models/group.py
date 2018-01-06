from flask.ext.login import UserMixin

from scytale.models import db, bcrypt, Point


class Group(UserMixin, db.Model):
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    def get_id(self):
        return str(self.gid)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).hex()

    def check_password(self, candidate):
        return bcrypt.check_password_hash(bytes.fromhex(self.password), candidate)

    def give_point(self, score, reason, max=0):
        p = Point()
        p.group = self
        p.score = score
        p.reason = reason
        db.session.add(p)
        return p
