#!/usr/bin/env python3
'''
    Emulate user login and detect user locale with Flask and Babel.
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__, template_folder='templates')
babel_instance = Babel(app)

class Config(object):
    '''
        Babel configuration.
    '''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user() -> dict:
    '''
        Fetch user information based on the user ID provided in the URL parameter.
    '''
    user_id = request.args.get('login_as')
    return users.get(int(user_id)) if user_id and int(user_id) in users else None

@app.before_request
def before_request():
    '''
        Set the user as a global variable on flask.g.user.
    '''
    g.user = get_user()

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    '''
        Render template with a welcome message based on the user's login status.
    '''
    welcome_message = _('logged_in_as', username=g.user['name']) if g.user else _('not_logged_in')
    return render_template('5-index.html', welcome_message=welcome_message)

@babel_instance.localeselector
def get_locale() -> str:
    '''
        Get user locale from URL parameters or default to accept languages.
    '''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run()
