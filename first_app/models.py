from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DateTime, BOOLEAN
from first_app.db import Base
import datetime
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
    def phone_num(self, phone_):
        if phone_ != self.phone_number:
            return{"error":"error"}
class Post(Base):
    __tablename__= 'post'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    created = Column(TIMESTAMP())
    body = Column(Text(), unique=False)
    title = Column(Text(), unique=False)
    deleted = Column(BOOLEAN)
    def __init__(self,author_id=None,created=None, title=None, body=None, deleted=None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.deleted = deleted
    def __repr__(self):
        return f'<Author id {self.author_id}>'