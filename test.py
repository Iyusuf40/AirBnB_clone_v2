#!/usr/bin/python3
from models import storage

from models.state import State

def get_s(dct, id):
    for item in dct:
        if id in item:
            return dct[item]

states = storage.all(State)

id = "b2e18b90-36bf-4db6-8212-8def3487cf17"
ps = get_s(states, id)
print(ps.cities)
for itm in ps.cities:
    print(str(itm))
