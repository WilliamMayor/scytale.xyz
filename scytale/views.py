import os

from flask import Blueprint, render_template

views = Blueprint('views', __name__, template_folder='templates')

def template(name, **kwargs):
    return render_template(name, **kwargs)

@views.route('/')
def home():
    return template('home.html')

@views.route('/padding/')
def padding():
    return template('padding.html')

@views.route('/modulo/')
def modulo():
    return template('modulo.html')