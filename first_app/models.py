from sqlalchemy import Column, Integer, String, Text
from first_app.db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone_number = Column(Text(), unique =True)
    first_name = Column(Text(), unique =False)
    second_name = Column(Text(), unique =False)
    password = Column(Text(), unique =False)
    def __init__(self, phone_number=None, first_name=None, second_name=None, password=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.second_name = second_name
        self.password = password
    def __repr__(self):
        return f'<User {self.phone_number}>'
    def user_info(self):
        return f"{self.first_name}, {self.second_name}, {self.phone_number}"