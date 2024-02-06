#!/usr/bin/env python3
'''
    Use Babel to determine user locale.
'''

from flask_babel import Babel, _
from flask import Flask, render_template, request, g

app = Flask(__name__, template_folder='templates')
babel_instance = Babel(app)

class ConfigObject:
    '''
        Configuration for Babel.
    '''
    LANGUAGES = ['en', 'fr']
    DEFAULT_LOCALE = 'en'
    DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(ConfigObject)

users_data = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def retrieve_user_locale() -> str:
    '''
        Retrieve user's preferred locale.
    '''
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return None

@app.before_request
def before_request():
    '''
        Operations performed before each request.
    '''
    login_as = request.args.get('login_as')
    g.user = users_data.get(int(login_as)) if login_as and int(login_as) in users_data else None

@app.route('/', methods=['GET'], strict_slashes=False)
def render_index() -> str:
    '''
        Render template for Babel usage.
    '''
    return render_template('6-index.html')

@babel_instance.localeselector
def select_locale() -> str:
    '''
        Select the appropriate locale for translation.
    '''
    # Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Get user's preferred locale
    user_locale = retrieve_user_locale()
    if user_locale:
        return user_locale

    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run()
