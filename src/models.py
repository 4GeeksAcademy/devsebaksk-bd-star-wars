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
    favorites = relationship("Favorites", back_populates="user")


    def serialize(self):
        return {"id":self.id,
                "username":self.username,
                "firstname":self.firstname,
                "lastname":self.lastname,
                "email":self.email
                }

class Planets (db.Model):

    __tablename__='planets'


    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    terrain: Mapped [str] = mapped_column(String(250), nullable=False)
    climated: Mapped [str] = mapped_column(String(250), nullable=False)
    diameter: Mapped [int] = mapped_column(Integer, nullable=True)
    #Relaciones


    

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climated": self.climated,
            "diameter": self.diameter
        }
    
    

class People ( db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    birth_year: Mapped[str]= mapped_column(String(250), nullable=False)
    height : Mapped[int]= mapped_column(Integer, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(250), nullable=False)
    planet_id: Mapped[int] = mapped_column(Integer, nullable=False)
    #Relaciones

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "eye_color": self.eye_color,
            "planet_id": self.planet_id
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "planet_id": self.planet_id
    }
    user = relationship("User", back_populates="favorites")