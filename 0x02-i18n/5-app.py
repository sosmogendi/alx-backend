#!/usr/bin/env python3
'''
    User locale detection and login emulation with Flask and Babel.
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__, template_folder='templates')
babel_instance = Babel(app)

class Config(object):
    '''
        Babel configuration.
    '''
    SUPPORTED_LANGUAGES = ['en', 'fr']
    DEFAULT_LOCALE = 'en'
    DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def fetch_user() -> Union[dict, None]:
    '''
        Fetch user information based on user ID provided in the URL parameter.
    '''
    try:
        login_as = request.args.get('login_as', None)
        if login_as:
            return users.get(int(login_as))
        else:
            return None
    except Exception:
        return None

@app.before_request
def before_request():
    '''
        Set the user as a global variable on flask.g.user.
    '''
    user = fetch_user()
    g.current_user = user if user else None

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    '''
        Render template with a welcome message based on the user's login status.
    '''
    welcome_message = _('logged_in_as', username=g.current_user['name']) if g.current_user else _('not_logged_in')
    return render_template('5-index.html', welcome_message=welcome_message)

@babel_instance.localeselector
def get_locale() -> str:
    '''
        Get user locale from URL parameters or default to accept languages.
    '''
    locale = request.args.get('locale')
    if locale in app.config['SUPPORTED_LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'])

if __name__ == '__main__':
    app.run()
