from app import app
from models import db, Planets, Vehicles, Characters

with app.app_context():
    
    # Lista de planetas de SW
    planets = [
        Planets(
            name="Tatooine", 
            climate="arid", 
            diameter=10465, 
            population=200000
        ),
        Planets(
            name="Coruscant", 
            climate="temperate", 
            diameter=12240, 
            population=100000
        ),
        Planets(
            name="Hoth",
            climate="frozen", 
            diameter=7200, 
            population=0
        )  
    ]
    if not Planets.query.first():
        db.session.add_all(planets)
        db.session.commit()


    # Lista de vehículos de SW

    vehicles = [
        Vehicles(
            name="X-wing starfighter",
            crew=1,
            cargo_capacity=110,
            manufacturer="Incom Corporation"
        ),
        
        Vehicles(
            name="Millennium Falcon",
            crew=4,
            cargo_capacity=100000,
            manufacturer="Corellian Engineering Corporation"
        ),
        
        Vehicles(
            name="Imperial AT-AT",
            crew=5,
            cargo_capacity=1000,
            manufacturer="Kuat Drive Yards"
        )
    ]

    if not Vehicles.query.first():
        db.session.add_all(vehicles)
        db.session.commit()

    # Lista de personajes de SW 

    characters = [
        Characters(
            name="Luke Skywalker 2",
            gender="male",
            birth_year="19BBY",
            height=172,
            eye_color="blue"
        ),
        Characters(
            name="Princess Leia Organa",
            gender="female",
            birth_year="19BBY",
            height=150,
            eye_color="brown"
        ),
        Characters(
            name="Darth Vader",
            gender="male",
            birth_year="41.9BBY",
            height=202,
            eye_color="yellow"
        )
    ]

    
    if not Characters.query.first():
        db.session.add_all(characters)
        db.session.commit()
