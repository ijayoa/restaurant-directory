import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'  # creates new table
    name = Column(String(89), nullable=False)  # create tables columns
    description = Column(String(250), nullable=False)  # create tables columns
    stars = Column(Integer, nullable=False)  # create tables columns
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        # returns obejct data in easily serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'stars' : self.stars,
            'id' : self.id,
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'  # creates new table
    name = Column(String(89), nullable=False)  # create tables columns
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restuarant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # returns obejct data in easily serializable format
        return {
            'name' : self.name,
            'price' : self.price,
            'description' : self.description,
            'course' : self.course,
            'id' : self.id,
        }

engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)