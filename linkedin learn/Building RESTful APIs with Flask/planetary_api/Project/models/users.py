from sqlalchemy import Column, Integer, String
from .base import db, ma

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(84))
    last_name = Column(String(84))
    email = Column(String(84))
    password = Column(String(84))   

    class UserSchema(ma.Schema):
        class Meta:
            fields = ('id', 'first_name', 'last_name', 'email', 'password')