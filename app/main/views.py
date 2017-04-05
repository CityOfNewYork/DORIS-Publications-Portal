from flask import (
    current_app,
    make_response,
    render_template,
    redirect,
    url_for,
    Blueprint,
)
from flask_login import login_user, logout_user
from flask_wtf.csrf import generate_csrf
from app.models.auth_user import AuthUser

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Sends the CSRF token from server to client as a cookie so that the client can scrape it out
    of the cookie and attach it to the X-CSRFToken header to send back to the server.
    http://stackoverflow.com/questions/20504846/why-is-it-common-to-put-csrf-prevention-tokens-in-cookies
    """
    response = make_response(render_template('index.html'))
    response.headers.set('Set-Cookie',
                         'csrf_token={csrf_token}; Max-Age={max_age}'.format(
                             csrf_token=generate_csrf(),
                             max_age=current_app.config['WTF_CSRF_TIME_LIMIT']))
    return response


@main.route('/login')
def login():
    user = AuthUser.query.first()
    if user is None:
        from app.database import db
        user = AuthUser(
            'GUIDXXX',
            'EDIRSSO',
            'Dirk',
             None,
            'Diggler',
            'dd@email.com',
            False,
            False
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for("main.index"))


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.index"))
