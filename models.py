from datetime import datetime

import os
from sqlalchemy import Column, ForeignKey, Integer, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer, String,BigInteger,DateTime
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine(os.getenv("POSTGRES_URL"))
base = declarative_base()
conn = engine.connect()
Session = sessionmaker()
my_session = Session(bind=engine)

spotted = Table('spotted', base.metadata,
    Column('animal_id', ForeignKey('animals.id'), primary_key=True),
    Column('location_id', ForeignKey('locations.locations_number'), primary_key=True)
)

class Animal(base):
    __tablename__= 'animals'

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    genus_id = Column(BigInteger, ForeignKey('genus.id'))
    gender = Column() #Gedanken machen
    estimated_age = Column(Integer)
    estimated_weight = Column(float)
    estimated_size = Column(float)
    location = relationship(
        "Location",
        secondary= spotted,
        back_populates="animals"
    )

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
    animal = relationship(
        "Animal",
        secondary= spotted,
        back_populates="locations"
    )

    def __init__(self, short_title, description):
        self.short_title = short_title
        self.description = description

class genus(base):
    __tablename__='genus'

    id = Column(BigInteger, primary_key=True,autoincrement=True)
    species_name = Column(String(25), nullable=False)
