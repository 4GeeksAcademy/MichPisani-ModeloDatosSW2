from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user" 

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable= False)
    name: Mapped[str] = mapped_column(String(50), nullable= False)
    lastname: Mapped[str] = mapped_column(String(50), nullable= False)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    favourites=relationship("Favourites", back_populates="user", cascade = "all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "subscription_date": self.subscription_date
        }
    
    
    def serialize_favourites(self):
        return {
            "user_id": self.id,
            "favourites": [favourite.serialize_all() for favourite in self.favourites]
        }
    

class Characters(db.Model):
    __tablename__="character" 

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable= False, unique=True)
    gender: Mapped[str] = mapped_column(nullable= False)
    birth_year: Mapped[str] = mapped_column(String(50))
    height: Mapped[int]
    eye_color: Mapped[str]

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "eye_color":self.eye_color
        }
    
    favourites=relationship("Favourites", back_populates="character")
    
class Vehicles (db.Model):
    __tablename__="vehicle" 

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable= False, unique=True)
    crew: Mapped[int] 
    cargo_capacity: Mapped[int]
    manufacturer: Mapped[str] = mapped_column(String(50))


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "crew": self.crew,
            "cargo_capacity": self.cargo_capacity,
            "manufacturer": self.manufacturer,
        }
    
    favourites=relationship("Favourites", back_populates="vehicle")

class Planets (db.Model):
    __tablename__="planet" 

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable= False, unique=True)
    climate: Mapped[str] = mapped_column(String(50))
    diameter: Mapped[int]
    population: Mapped[int] 


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population,
        }
    
    favourites=relationship("Favourites", back_populates="planet")

class Favourites (db.Model):
    __tablename__="favourite" 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey("vehicle.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey("character.id"), nullable=True)

    def serialize_all(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
            "character_id": self.character_id,
        }
    

    user=relationship("User", back_populates="favourites")
    planet=relationship("Planets", back_populates="favourites")
    vehicle=relationship("Vehicles", back_populates="favourites")
    character=relationship("Characters", back_populates="favourites")


    
 
    
