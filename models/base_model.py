#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type
from sqlalchemy.dialects.mysql import VARCHAR

if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """A base class for all hbnb models"""

    if storage_type == 'db':
        id = Column(String(60),
                    primary_key=True)
        created_at = Column(DateTime(), default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime(), default=datetime.utcnow(),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        from models import storage_type
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if storage_type == 'db':
                self.id = str(uuid.uuid4())
            else:
                if 'id' not in kwargs:
                    kwargs['id'] = str(uuid.uuid4())
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime\
                        .fromisoformat(kwargs['updated_at'])
                kwargs['created_at'] = datetime\
                    .fromisoformat(kwargs['created_at'])
            else:
                if storage_type != 'db':
                    kwargs['updated_at'] = datetime.now()
                    kwargs['created_at'] = datetime.now()
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            dictionary.pop('_sa_instance_state')
        if self.__class__.__name__ == 'Place':
            dictionary['amenity_ids'] = self.amenity_ids
        return dictionary

    def delete(self):
        """delete self"""
        from models import storage
        storage.delete(self)
