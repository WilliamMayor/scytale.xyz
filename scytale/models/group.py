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

    def give_point(self, score, reason, message):
        p = Point()
        p.group = self
        p.message = message
        p.score = score
        p.reason = reason
        db.session.add(p)
        return p

    def knows_plaintext(self, message):
        if message.group_id == self.gid:
            return True
        reasons = {
            "Requested plaintext {0}".format(message.mid),
            "Hacked Message {0}".format(message.mid)}
        for p in self.points:
            if p.reason in reasons:
                return True
        return False

    def knows_key(self, message):
        if message.group_id == self.gid:
            return True
        if message.group.name == "Billy":
            # Messages from worksheets
            return True
        return any([
            p.reason == "Hacked Key {0}".format(message.key_id)
            for p in self.points])
