#!/usr/bin/python3
"""tests relationship between State and City Models"""
from models.state import State
from models.city import City
from models import storage

state_1 = State(name='Sokoto', weather='tropicsl')
storage.new(state_1)
state_2 = State(name='Lagos', weather='erh I dunno')
storage.new(state_2)
city_1 = City(name='Ikeja', state='Lagos', state_id=state_2.id)
storage.new(city_1)
city_2 = City(name='Sokoto', state='Sokoto', state_id=state_1.id)
storage.new(city_2)
city_3 = City(name='Victoria Island', state='Lagos', state_id=state_2.id)
storage.new(city_3)

def print_cities(state):
    """gets a state object and print cities associated with it"""
    print("State: ", state.name)
    print()
    for city in state.cities:
        print(city)
    print()

if __name__ == '__main__':
    print_cities(state_1)
    print_cities(state_2)
