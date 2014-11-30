import os

import logging
from logging import StreamHandler

from flask import Flask

from views import views
from assets import assets
from login import manager
from models import db, bcrypt

def create_app(config=None):
    app = Flask('scytale')
    app.config.from_object('scytale.config')
    app.config.update({k: v for k, v in os.environ.iteritems() if k in app.config})
    if config is not None:
        app.config.update(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(StreamHandler())
    
    assets.init_app(app)
    db.init_app(app)
    manager.init_app(app)
    bcrypt.init_app(app)
    
    app.register_blueprint(views)
    return app