from flask import (
    current_app,
    make_response,
    render_template,
    Blueprint,
)
from flask_wtf.csrf import generate_csrf

main = Blueprint('main', __name__)


# all routes accessible by react router should be listed here!
@main.route('/')
@main.route('/faq')
@main.route('/about')
@main.route('/contact')
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
