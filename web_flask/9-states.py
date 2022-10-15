#!/usr/bin/python3
""" a simple flask app """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_session(f):
    """ closes db session """
    storage.close()


@app.route('/states', strict_slashes=False)
def state_list():
    """ gets all the states in db """
    from models.state import State
    dct = {}
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route('/states/<string:id>', strict_slashes=False)
def state_with_id(id):
    """ gets all the states in db with id == id """
    from models.state import State
    key = "State." + id
    states = storage.all(State)
    try:
        state = states[key]
    except KeyError:
        state = None
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
