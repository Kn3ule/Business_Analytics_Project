from datetime import datetime

import os
from sqlalchemy import Column, ForeignKey, Integer, create_engine, Table
from sqlalchemy.sql.sqltypes import Integer, String,BigInteger,DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine(os.getenv("POSTGRES_URL"))
base = declarative_base()
conn = engine.connect()
Session = sessionmaker()
my_session = Session(bind=engine)

'''
spotted = Table('spotted', base.metadata,
    Column('animal_id', ForeignKey('animals.id'), primary_key=True),
    Column('location_id', ForeignKey('locations.location_number'), primary_key=True),
    Column('spotted_date', DateTime(timezone=True), nullable=False),
    Column('spotted_time', DateTime(timezone=True), nullable=False)
)
'''

class Observation(base):
    __tablename__ = 'observations'

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    animal_id = Column(BigInteger, ForeignKey('animals.id'), nullable=False)
    location_id = Column(BigInteger, ForeignKey('locations.location_number'), nullable=False)
    observation_time = Column(DateTime(timezone=True), nullable=False)

    animal = relationship('Animal', backref='observations')
    location = relationship('Location', backref='observations')

    def __init__(self, animal, location, observation_time):
        self.animal = animal
        self.location = location
        self.observation_time = observation_time


class Animal(base):
    __tablename__= 'animals'

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    genus_id = Column(BigInteger, ForeignKey('genus.id'))
    gender = Column(String, nullable=False) #Gedanken machen
    estimated_age = Column(Integer)
    estimated_weight = Column(Float)
    estimated_size = Column(Float)

    locations = relationship("Location", secondary="observations", viewonly=True)

    def __init__(self, genus_id, gender, estimated_age, estimated_weight, estimated_size):
        self.genus_id =genus_id
        self.gender = gender
        self.estimated_age = estimated_age
        self.estimated_weight = estimated_weight
        self.estimated_size = estimated_size

class Location(base):
    __tablename__='locations'

    location_number = Column(BigInteger, primary_key=True,autoincrement=True)
    short_title = Column(String(20), nullable=False)
    description = Column(String, nullable=False)

    animals = relationship("Animal", secondary="observations", viewonly=True)

    def __init__(self, short_title, description):
        self.short_title = short_title
        self.description = description

class genus(base):
    __tablename__='genus'

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    species_name = Column(String(25), nullable=False)


def create_tables():
    base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
