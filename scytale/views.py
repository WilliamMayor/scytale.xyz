import hashlib
from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from scytale.ciphers import Checkerboard, Fleissner, MixedAlphabet, Myszkowski, Playfair, RailFence, Trifid
from scytale.forms import SignUpForm, SignInForm, MessageForm, HackForm
from scytale.models import db, Group, Message, Point

bp = Blueprint("bp", __name__, template_folder="templates")


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        g = Group()
        g.name = form.name.data
        g.set_password(form.password.data)
        db.session.add(g)
        db.session.commit()
        login_user(g)
        return redirect(url_for(".home"))
    return render_template("signup.html", form=form)


@bp.route("/signin/", methods=["GET", "POST"])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        g = Group.query.filter_by(name=form.name.data).first()
        login_user(g)
        return redirect(url_for(".home"))
    return render_template("signin.html", form=form)


@bp.route("/signout/")
def signout():
    logout_user()
    return redirect(url_for(".home"))


@bp.route("/messages/send/", methods=["GET", "POST"])
@login_required
def messages_send():
    form = MessageForm()
    if form.validate_on_submit():
        m = Message()
        m.group = current_user
        m.cipher = form.cipher.data
        m.key = form.key.data
        m.plaintext = form.plaintext.data
        m.ciphertext = form.ciphertext.data
        db.session.add(m)
        current_user.give_point(1, "Sent Message", max=5)
        db.session.commit()
        flash("Message Sent!")
        form = MessageForm(None, cipher=m.cipher, key=m.key)
    return render_template("messages/send.html", form=form)


@bp.route("/messages/read/")
@login_required
def messages_read():
    messages = defaultdict(list)
    for m in Message.query.all():
        messages[m.group.name].append(m)
    return render_template("messages/read.html", messages=messages)


@bp.route("/messages/hack/<int:mid>/", methods=["GET", "POST"])
@login_required
def messages_hack(mid):
    message = Message.query.get(mid)
    if message is None:
        abort(404)
    see_plaintext = message.group == current_user or any([
        p.reason in [
            "Requested plaintext {0}".format(mid),
            "Hacked Message {0}".format(mid)]
        for p in current_user.points])
    see_key = message.group == current_user or message.group.name == "Billy" or any([
        p.reason == "Hacked Key {0}".format(hashlib.md5(message.key.encode()).hexdigest())
        for p in current_user.points])
    form = HackForm(message=message)
    if form.validate_on_submit():
        if form.key.data and not see_key:
            points = current_user.give_point(20, "Hacked Key {0}".format(hashlib.md5(message.key.encode()).hexdigest()), max=1)
            flash("Key Hacked! ({0} points)".format(points))
        if form.plaintext.data and not see_plaintext:
            reason = "Hacked Message {0}".format(mid)
            if message.group.name == "Billy":
                reason = "Hacked Billy's Message"
            points = current_user.give_point(5, reason, max=1)
            flash("Message Hacked! ({0} points)".format(points))
        db.session.commit()
        return redirect(url_for(".messages_hack", mid=mid))
    return render_template(
        "messages/hack.html",
        message=message, form=form,
        see_plaintext=see_plaintext, see_key=see_key)


@bp.route("/messages/plaintext/<int:mid>/", methods=["GET", "POST"])
@login_required
def messages_plaintext(mid):
    message = Message.query.get(mid)
    if message is None:
        abort(404)
    if message.group == current_user:
        abort(403)
    points = current_user.give_point(-5, "Requested plaintext {0}".format(mid), max=1)
    flash("Requested Plaintext ({0} points)".format(points))
    db.session.commit()
    return redirect(url_for(".messages_hack", mid=mid))


@bp.route("/leaderboard/")
def leaderboard():
    groups = defaultdict(lambda: {"total": 0, "points": []})
    for p in Point.query.all():
        groups[p.group.name]["name"] = p.group.name
        groups[p.group.name]["total"] += p.score
        groups[p.group.name]["points"].append(p)
    return render_template("leaderboard.html", groups=groups.values())


@bp.route("/ciphers/checkerboard/")
def checkerboard():
    cipher = Checkerboard()
    return render_template("ciphers/checkerboard.html", cipher=cipher)


@bp.route("/ciphers/fleissner/")
def fleissner():
    cipher = Fleissner()
    return render_template("ciphers/fleissner.html", cipher=cipher)


@bp.route("/ciphers/mixed/")
def mixed():
    cipher = MixedAlphabet()
    return render_template("ciphers/mixed.html", cipher=cipher)


@bp.route("/ciphers/myszkowski/")
def myszkowski():
    cipher = Myszkowski()
    return render_template("ciphers/myszkowski.html", cipher=cipher)


@bp.route("/ciphers/playfair/")
def playfair():
    cipher = Playfair()
    return render_template("ciphers/playfair.html", cipher=cipher)


@bp.route("/ciphers/railfence/")
def railfence():
    cipher = RailFence()
    return render_template("ciphers/railfence.html", cipher=cipher)


@bp.route("/ciphers/trifid/")
def trifid():
    cipher = Trifid()
    return render_template("ciphers/trifid.html", cipher=cipher)
