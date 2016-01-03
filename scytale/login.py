from flask.ext.login import LoginManager

from scytale.models import Group

login_manager = LoginManager()
login_manager.login_view = "bp.signin"


@login_manager.user_loader
def load_user(gid):
    return Group.query.get(int(gid))


def init_app(app):
    login_manager.init_app(app)
