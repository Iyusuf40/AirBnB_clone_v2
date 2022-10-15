#!/usr/bin/python3
""" a simple flask app """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_session(f):
    """ closes db session """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_of_a_state():
    """ gets all the cities associated with a state from db """
    from models.state import State
    dct = {}
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
