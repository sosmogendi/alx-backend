#!/usr/bin/env python3
'''
    Use Babel to get user locale.
'''

from flask import Flask, render_template, request
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

@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world() -> str:
    '''
        Render template for Babel usage.
    '''
    return render_template('4-index.html', _=_)

@babel_instance.localeselector
def get_locale() -> str:
    '''
        Get user locale.
    '''
    if 'locale' in request.args:
        locale = request.args.get('locale')
        if locale in app.config['SUPPORTED_LANGUAGES']:
            return locale
    return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'])

if __name__ == '__main__':
    app.run()
