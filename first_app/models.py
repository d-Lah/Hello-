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
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    phone_number = db.Column(Text(), unique = True)
    first_name = db.Column(Text(), unique =False)
    second_name = db.Column(Text(), unique =False)
    password = db.Column(Text(), unique =False)
        
    def __repr__(self):
        return f'<User {self.phone_number}>'
    
    def user_info(self):
        return f"{self.first_name} {self.second_name}, {self.phone_number}"
    
    def full_name(self):
        return f"{self.first_name} {self.second_name}"


class FileUpload(db.Model):
    __tablename__ = 'file_upload'
    id = Column(Integer,primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    file_type = Column(Text(), unique = False)
    url = Column(String())
    post = relationship("Post", back_populates="file")
    deleted = Column(Boolean(), default=False)

class Comment(db.Model):
    __tablename__='comments'
    id = Column(Integer,primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    user_name = Column(Text(), ForeignKey("user.first_name"),nullable=False)
    created = Column(TIMESTAMP())
    text = Column(Text(100),nullable=False)
    deleted = Column(Boolean(),default=False)

    def __repr__(self):
        return f'<Author id {self.author_id}>'

class Post(db.Model):
    __tablename__= 'post'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_name = Column(Text(), ForeignKey("user.first_name"),nullable=False)
    created = Column(TIMESTAMP())
    body = Column(Text(), unique=False)
    title = Column(Text(), unique=False)
    deleted = Column(Boolean(),default=False)

    file_id = Column(Integer, ForeignKey("file_upload.id"))
    file = relationship("FileUpload", back_populates="post", primaryjoin=FileUpload.id==file_id)
    
    comments = relationship("Comment", primaryjoin="and_(Post.id == Comment.post_id,Comment.deleted==False)", backref = "post")

    def __repr__(self):
        return f'<Author id {self.author_id}>'
