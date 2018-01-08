import random
from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask.ext.login import login_user, logout_user, current_user, login_required

from scytale.ciphers import Checkerboard, Fleissner, MixedAlphabet, Myszkowski, Permutation, OneTimePad, Playfair, RailFence, Trifid
from scytale.exceptions import ScytaleError
from scytale.forms import SignUpForm, SignInForm, MessageForm, HackForm
from scytale.models import db, Group, Message, Point

CIPHERS = {
    "checkerboard": Checkerboard,
    "fleissner": Fleissner,
    "mixed": MixedAlphabet,
    "myszkowski": Myszkowski,
    "permutation": Permutation,
    "otp": OneTimePad,
    "playfair": Playfair,
    "railfence": RailFence,
    "trifid": Trifid,
}

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
@login_required
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
        current_user.give_point(1, "Sent Message", m)
        db.session.commit()
        flash("Message Sent!")
        form = MessageForm(None, cipher=m.cipher, key=m.key)
    return render_template("messages/send.html", form=form)


@bp.route("/messages/read/")
@login_required
def messages_read():
    query = Message.query
    group = request.args.get("group")
    if group is not None:
        group = Group.query.filter(Group.name == group).first()
        query = query.filter(Message.group == group)
    cipher = request.args.get("cipher")
    if cipher is not None:
        query = query.filter(Message.cipher == cipher)
    key_id = request.args.get("key")
    if key_id is not None:
        query = (m for m in query if m.key_id == key_id)
    return render_template("messages/read.html", messages=query)


@bp.route("/messages/hack/<int:mid>/", methods=["GET", "POST"])
@login_required
def messages_hack(mid):
    message = Message.query.get(mid)
    if message is None:
        abort(404)
    see_plaintext = current_user.knows_plaintext(message)
    see_key = current_user.knows_key(message)
    form = HackForm(message=message)
    if form.validate_on_submit():
        if form.key.data and not see_key:
            reason = "Hacked Key {0}".format(message.key_id)
            current_user.give_point(20, reason, message)
            flash("Key Hacked! (20 points)")
        if form.plaintext.data and not see_plaintext:
            reason = "Hacked Message {0}".format(mid)
            current_user.give_point(5, reason, message)
            flash("Message Hacked! (5 points)")
        db.session.commit()
        return redirect(url_for(".messages_hack", mid=mid))
    return render_template(
        "messages/hack.html",
        message=message, form=form,
        see_plaintext=see_plaintext, see_key=see_key)


@bp.route("/leaderboard/")
def leaderboard():
    groups = defaultdict(lambda: {"total": 0, "points": []})
    for p in Point.query.all():
        groups[p.group.name]["name"] = p.group.name
        groups[p.group.name]["total"] += p.score
        groups[p.group.name]["points"].append(p)
    return render_template("leaderboard.html", groups=groups.values())


@bp.route("/ciphers/<cipher>/", methods=["GET", "POST"])
def ciphers(cipher):
    if request.method == "POST":
        plaintext = request.form.get("plaintext")
        key = request.form.get("key")
        try:
            c = CIPHERS[cipher](key=key)
            return c.encrypt(plaintext)
        except ScytaleError as e:
            return str(e), 400
        except Exception:
            return "Something went wrong!", 400
    c = CIPHERS[cipher]()
    return render_template("ciphers/{}.html".format(cipher), cipher=c)


def generate_key(alphabet, known_key):
    randomised = list(set(alphabet) - set(known_key))
    random.shuffle(randomised)
    for k in known_key:
        if k == '?':
            yield randomised.pop()
        else:
            yield k


@bp.route("/cryptanalysis/mixed/", methods=["GET", "POST"])
def cryptanalysis_mixed():
    if request.method == "POST":
        known_key = request.form.get('known_key')
        generated_key = request.form.get('generated_key')
        use_generated = bool(request.form.get('use_generated'))
        ciphertexts = request.form.get('ciphertexts', '').strip().splitlines()
        plaintexts = request.form.get('plaintexts', '').strip().splitlines()
        cipher = MixedAlphabet(known_key, wildcard='?')
        if request.form.get('action') == 'Generate Key':
            use_generated = True
            generated_key = "".join(generate_key(cipher.alphabet, known_key))
        if use_generated:
            cipher = MixedAlphabet(generated_key, wildcard='?')
        plaintexts = [cipher.decrypt(c) for c in ciphertexts]
    else:
        known_key = generated_key = '?' * 27
        use_generated = False
        plaintexts = []
        ciphertexts = []
    return render_template(
        "cryptanalysis/mixed.html",
        known_key=known_key,
        generated_key=generated_key,
        use_generated=use_generated,
        plaintexts=plaintexts,
        ciphertexts=ciphertexts)
