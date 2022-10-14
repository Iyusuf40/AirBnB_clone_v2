#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String,\
    ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models import storage_type
from sqlalchemy.dialects.mysql import VARCHAR


if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', ForeignKey('places.id')),
                          Column('amenity_id', ForeignKey('amenities.id'))
                          )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60).with_variant(VARCHAR(60, charset="latin1"),
                     "mysql"), ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60).with_variant(VARCHAR(60, charset="latin1"),
                     "mysql"), ForeignKey("users.id"),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0,
                          nullable=False)
    number_bathrooms = Column(Integer, default=0,
                              nullable=False)
    max_guest = Column(Integer, default=0,
                       nullable=False)
    price_by_night = Column(Integer, default=0,
                            nullable=False)
    latitude = Column(Float())
    longitude = Column(Float())
    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship('Review', back_populates='place',
                           cascade='all, delete, delete-orphan')
    amenities = relationship('Amenity',
                             secondary='place_amenity',
                             back_populates='place_amenities')
    amenity_ids = []

    def __get_reviews(self):
        """returns a list of all reviews with place_id
        equal to self.id"""
        from models import storage
        from models.review import Review
        lst = []

        for obj in storage.all(Review).values():
            if obj.place_id == self.id:
                lst.append(obj)

        return lst

    def __get_amenities(self):
        """gets amenities associated with self"""
        from models import storage
        from models.amenity import Amenity
        lst = []
        for obj in storage.all(Amenity).values():
            if obj.id in self.amenity_ids:
                lst.append(obj)
        return lst

    def __set_amenities(self, obj):
        """sets amenity associated with self"""
        if obj.__class__.__name__ == 'Amenity':
            self.amenity_ids.append(obj.id)
            self.save()

    if storage_type != 'db':
        @property
        def reviews(self):
            """returns reviews of a place"""
            return self.__get_reviews()

        @property
        def amenities(self):
            """returns amenities associated with place"""
            return self.__get_amenities()

        @amenities.setter
        def amenities(self, obj):
            """sets an amenity for a place"""
            self.__set_amenities(obj)
