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


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """returns C <text>"""
    if (type(text) is str):
        text = text.replace('_', ' ')
        return "C " + text
    from flask import Abort
    Abort(404)


@app.route('/python/', redirect_to='python/is_cool', strict_slashes=False)
def python_re_route(text="is cool"):
    """returns Python <text>"""
    pass


@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """returns Python <text>"""
    text = text.replace('_', ' ')
    return "Python " + text


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """checks if n is number"""
    return str(n) + " is number"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
