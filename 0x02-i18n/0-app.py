#!/usr/bin/env python3
'''
    Module for Babel i18n.
'''

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'], strict_slashes=False)
def helloWorld() -> str:
    '''
        Render template for Babel usage.
    '''
    return render_template('0-index.html', title='Welcome to Holberton', header='Hello world')


if __name__ == '__main__':
    app.run()
