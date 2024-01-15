from sqlalchemy import Column, Integer, String, Float
from .base import db, ma

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String(84))
    planet_type = Column(String(84))
    home_star = Column(String(84))
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

    def __init__(self, planet_name: str, planet_type: str, home_star: str, mass: float, radius: float, distance: float):
        self.planet_name = planet_name
        self.planet_type = planet_type
        self.home_star = home_star
        self.mass = mass
        self.radius = radius
        self.distance = distance

    class PlanetSchema(ma.Schema):
        class Meta:
            fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

