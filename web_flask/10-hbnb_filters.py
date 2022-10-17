#!/usr/bin/python3
""" a simple flask app """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_session(f):
    """ closes db session """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb():
    """ renders template with data from db """
    from models.state import State
    from models.amenity import Amenity
    states = storage.all(State)
    states = [obj for obj in states.values()]
    amenities = storage.all(Amenity)
    amenities = [obj for obj in amenities.values()]
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
