from sqlalchemy import Column, Integer, String
from .base import db, ma

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(84))
    last_name = Column(String(84))
    email = Column(String(84))
    password = Column(String(84))   

    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    class UserSchema(ma.Schema):
        class Meta:
            fields = ('id', 'first_name', 'last_name', 'email', 'password')