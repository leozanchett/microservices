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

    class PlanetSchema(ma.Schema):
        class Meta:
            fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

