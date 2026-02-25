from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserInput(Base):
    __tablename__ = 'user_input'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    input_type = Column(String)  # text, image, video, file
    content = Column(Text)       # text or file path
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('UserProfile')

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    game_type = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('UserProfile')

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    description = Column(Text)
    status = Column(String)  # active, completed, etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('UserProfile')

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profile.id'))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('UserProfile')