import datetime
from .db import db
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Text,
                        TIMESTAMP,
                        DateTime,
                        Boolean,
                        ForeignKey)
class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    phone_number = Column(Text(), unique =True)
    first_name = Column(Text(), unique =False)
    second_name = Column(Text(), unique =False)
    password = Column(Text(), unique =False)
    
    def __init__(self, phone_number=None, 
                 first_name=None, 
                 second_name=None, 
                 password=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.second_name = second_name
        self.password = password
    
    def __repr__(self):
        return f'<User {self.phone_number}>'
    
    def user_info(self):
        return f"{self.first_name}, {self.second_name}, {self.phone_number}"

class Post(db.Model):
    __tablename__= 'post'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created = Column(TIMESTAMP())
    body = Column(Text(), unique=False)
    title = Column(Text(), unique=False)
    deleted = Column(Boolean(),default=False)
    file_id = Column(Integer, ForeignKey("file_upload.id"), nullable=True)

    def __init__(self,author_id=None,
                 created=None, title=None,
                 body=None,
                 deleted=None,
                 file_id=None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.deleted = deleted
        self.file_id = file_id
    def __repr__(self):
        return f'<Author id {self.author_id}>'

class Comment(db.Model):
    __tablename__='comments'
    id = Column(Integer,primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    created = Column(TIMESTAMP())
    text = Column(Text(100),nullable=False)
    deleted = Column(Boolean(),default=False)

    def __init__(self,author_id=None,
                    post_id=None,
                    created=None,
                    text=None,
                    deleted=None,
                    ):
        
        self.author_id = author_id
        self.post_id = post_id
        self.created = created
        self.text = text
        self.deleted = deleted
    def __repr__(self):
        return f'<Auth9or id {self.author_id}>'

class FileUpload(db.Model):
    __tablename__ = 'file_upload'
    id = Column(Integer,primary_key=True)
    url = Column(String())
    
    def __init__(self, url):
        self.url = url