#!/usr/bin/python3
""" a simple flask app """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_session(f):
    """ closes db session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def static_list():
    """ gets all the states in db """
    from models.state import State
    dct = {}
    states = storage.all(State)
    states = [ obj for obj in states.values() ]
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
