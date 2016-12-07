from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired

from scytale.ciphers import Checkerboard, Fleissner, MixedAlphabet, Myszkowski, OneTimePad, Playfair, RailFence, Trifid
from scytale.exceptions import ScytaleError
from scytale.models import Group


class SignInForm(Form):
    name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        g = Group.query.filter_by(name=self.name.data).first()
        if g is None:
            self.name.errors.append("Unknown Group: {0}".format(self.name.data))
            return False
        if not g.check_password(self.password.data):
            self.password.errors.append("Incorrect password")
            return False
        return True


class SignUpForm(Form):
    name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        g = Group.query.filter_by(name=self.name.data).first()
        if g is not None:
            self.name.errors.append("Group name taken: {0}".format(self.name.data))
            return False
        return True


class MessageForm(Form):
    cipher = SelectField("Cipher", choices=[
        ("Checkerboard", "Checkerboard"),
        ("Fleissner", "Fleissner"),
        ("Mixed Alphabet", "Mixed Alphabet"),
        ("Myszkowski", "Myszkowski"),
        ("One Time Pad", "One Time Pad"),
        ("Playfair", "Playfair"),
        ("Rail Fence", "Rail Fence"),
        ("Trifid", "Trifid")
    ])
    key = StringField("Key", validators=[DataRequired()])
    plaintext = TextAreaField("Plain Text", validators=[DataRequired()])
    ciphertext = TextAreaField("Cipher Text", validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        try:
            cipher = {
                "Checkerboard": Checkerboard,
                "Fleissner": Fleissner,
                "Mixed Alphabet": MixedAlphabet,
                "Myszkowski": Myszkowski,
                "One Time Pad": OneTimePad,
                "Playfair": Playfair,
                "Rail Fence": RailFence,
                "Trifid": Trifid
            }[self.cipher.data](key=self.key.data)
        except ScytaleError as se:
            self.key.errors.append("Invalid Key: {0}".format(se.args[0]))
            return False
        try:
            ciphertext = cipher.encrypt(self.plaintext.data)
            assert cipher.compare_ciphertext(ciphertext, self.ciphertext.data)
        except Exception:
            print("{} not equal to {}".format(ciphertext, self.ciphertext.data))
            self.ciphertext.errors.append("Incorrect ciphertext")
            return False
        return True


class HackForm(Form):
    key = StringField("Key")
    plaintext = StringField("Plain Text")

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message")
        super().__init__(*args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        result = True
        if self.key.data and self.key.data != self.message.key:
            self.key.errors.append("Incorrect key")
            result = False
        if self.plaintext.data:
            cipher = {
                "Checkerboard": Checkerboard,
                "Fleissner": Fleissner,
                "Mixed Alphabet": MixedAlphabet,
                "Myszkowski": Myszkowski,
                "One Time Pad": OneTimePad,
                "Playfair": Playfair,
                "Rail Fence": RailFence,
                "Trifid": Trifid
            }[self.message.cipher](key=self.message.key)
            if not cipher.compare_plaintext(self.plaintext.data, self.message.plaintext):
                print("{} not equal to {}".format(self.plaintext.data, self.message.plaintext))
                self.plaintext.errors.append("Incorrect plain text")
                result = False
        return result
