from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class SetupForm(Form):
    directory = StringField(u'Storage Directory', validators=[DataRequired()])


class ProjectForm(Form):
    name = StringField(u'Name', validators=[DataRequired()])
    directory = StringField(u'Directory', validators=[DataRequired()])

class TaskForm(Form):
    name = StringField(u'Name', validators=[DataRequired()])
