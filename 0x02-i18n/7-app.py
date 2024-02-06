#!/usr/bin/env python3
""" Module for trying out Babel i18n """

from flask_babel import Babel, _
from flask import Flask, render_template, request, g
import pytz
from typing import Union

app = Flask(__name__, template_folder='templates')
babel_instance = Babel(app)


class ConfigObject:
    """ Configuration Class for Babel """

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


def retrieve_user() -> Union[dict, None]:
    """ Returns a user dictionary or None if the ID cannot be found or if login_as was not passed."""
    try:
        login_as = request.args.get("login_as")
        user = users_data[int(login_as)]
    except Exception:
        user = None
    return user


@app.before_request
def before_request():
    """ Operations that happen before any request """
    user = retrieve_user()
    g.user = user


@app.route('/', methods=['GET'], strict_slashes=False)
def render_index() -> str:
    """ Renders a Basic Template for Babel Implementation """
    return render_template("7-index.html")


@babel_instance.localeselector
def select_locale() -> str:
    """ Select a language translation to use for that request """
    locale = request.args.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel_instance.timezoneselector
def select_timezone() -> str:
    """
    Find timezone parameter in URL parameters
    Find time zone from user settings
    Default to UTC
    """
    try:
        if request.args.get("timezone"):
            timezone = request.args.get("timezone")
            tz = pytz.timezone(timezone)

        elif g.user and g.user.get("timezone"):
            timezone = g.user.get("timezone")
            tz = pytz.timezone(timezone)
        else:
            timezone = app.config["DEFAULT_TIMEZONE"]
            tz = pytz.timezone(timezone)

    except pytz.exceptions.UnknownTimeZoneError:
        timezone = "UTC"

    return timezone


if __name__ == "__main__":
    app.run()
