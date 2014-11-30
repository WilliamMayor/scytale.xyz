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

@views.route('/affine/')
def affine():
    return template('affine.html')

@views.route('/fleissner/')
def fleissner():
    return template('fleissner.html')

@views.route('/mixed/')
def mixed():
    return template('mixed.html')

@views.route('/pigpen/')
def pigpen():
    return template('pigpen.html')

@views.route('/playfair/')
def playfair():
    return template('playfair.html')

@views.route('/singleletter/')
def singleletter():
    return template('singleletter.html')

@views.route('/checkerboard/')
def checkerboard():
    return template('checkerboard.html')

@views.route('/columnar/')
def columnar():
    return template('columnar.html')

@views.route('/myszkowski/')
def myszkowski():
    return template('myszkowski.html')

@views.route('/railfence/')
def railfence():
    return template('railfence.html')

@views.route('/route/')
def route():
    return template('route.html')

@views.route('/trifid/')
def trifid():
    return template('trifid.html')
