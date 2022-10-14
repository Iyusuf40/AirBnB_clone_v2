#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', back_populates='state',
                          cascade="all, delete, delete-orphan")

    def __get_cities(self):
        """returns all City objects associated with self"""
        from models import storage
        from models.city import City
        cities = storage.all(City)
        lst = []
        for obj in cities.values():
            if obj.state_id == self.id:
                lst.append(obj)
        return lst

    if storage_type != 'db':
        @property
        def cities(self):
            """returns get_cities"""
            #return self.__get_cities()
            pass
