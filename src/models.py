from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er


db = SQLAlchemy()

favorites_planets = Table ('favorites_planets', db.Model.metadata, 
            Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
            Column('planet_id', Integer, ForeignKey('planets.id'), primary_key=True)
            )

favorites_people = Table ('favorites_people', db.Model.metadata, 
            Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
            Column('people_id', Integer, ForeignKey('people.id'), primary_key=True)
            )

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(250), nullable= False)
    lastname: Mapped[str] = mapped_column(String(250), nullable= False)
    email: Mapped[str] = mapped_column(String(250), nullable = False)
    #Relaciones
    favorites_planets: Mapped[list['Planets']] = relationship('Planets',secondary = favorites_planets ,back_populates='favorite_users')
    favorites_people: Mapped[list['People']] = relationship('People',secondary = favorites_people ,back_populates='favorite_users')

    def serialize(self):
        return {"id":self.id, "username":self.username}

class Planets (db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    terrain: Mapped [str] = mapped_column(String(250), nullable=False)
    climated: Mapped [str] = mapped_column(String(250), nullable=False)
    diameter: Mapped [int] = mapped_column(Integer, nullable=True)
    #Relaciones
    peoples: Mapped[list['People']] = relationship('People', back_populates='planet_id')
    favorites_user: Mapped[list['User']] = relationship('User',secondary = favorites_planets ,back_populates='favorite_users')
    

class People ( db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    birth_year: Mapped[str]= mapped_column(String(250), nullable=False)
    height : Mapped[int]= mapped_column(Integer, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(250), nullable=False)
    #Relaciones
    planet_id: Mapped[int] = mapped_column(Integer, ForeignKey('planets.id'))
    favorites_user: Mapped[list['User']] = mapped_column(Integer,back_populates='favorite_users')


  