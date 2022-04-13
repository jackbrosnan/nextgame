# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Float, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, nullable=False)
    Title = Column('Title', Text)
    Genres = Column('Genres', Text)
    age_rating = Column('Age Rating', Text)
    platforms = Column('Platforms', Text)
    Summary = Column(Text)
    player_persp = Column('Player Perspective', Text)
    release_date = Column('Release Date', Text)
    images = Column('images', Text)
    cover = Column('CoverID', Text)

class User(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, ForeignKey('auth_user.id'), primary_key=True, nullable=False)
    pref_platforms = Column('Preferred Platforms', Text)
    liked_games = Column('Liked Games', Text)
    rec_game_ids = Column('Recommended Games', Text)