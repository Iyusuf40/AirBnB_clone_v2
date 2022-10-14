#!/usr/bin/python3
""" A simple flask app """


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """root route"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """hbnb route"""
    return "HBNB"


@app.route('/c/<string:text>', strict_slashes=False)
def c_route(text):
    """returns C is <text>"""
    if (text):
        text.replace('_', ' ')
        return "C " + text
    return "C"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
