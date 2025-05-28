import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile_picture = Column(String(250))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='user')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')

    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='comments')

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comments')

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='likes')

    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='likes')

# Diagram generator
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file.")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
