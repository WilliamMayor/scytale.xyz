from scytale.models import db


class Point(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    reason = db.Column(db.Text)

    group_id = db.Column(db.Integer, db.ForeignKey('group.gid'))
    group = db.relationship('Group', backref=db.backref('points', lazy='dynamic'))
