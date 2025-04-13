from sqlalchemy import (
    create_engine, Column, Integer, String, Date, ForeignKey, Table, Float, Text, Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

# Association Tables
movie_genre_table = Table(
    'movie_genre', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)

movie_person_role_table = Table(
    'movie_person_role', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('person_id', ForeignKey('people.id'), primary_key=True),
    Column('role', String, primary_key=True)  # e.g., actor, director, producer
)

movie_company_table = Table(
    'movie_company', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('company_id', ForeignKey('production_companies.id'), primary_key=True)
)

movie_keyword_table = Table(
    'movie_keyword', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)
    runtime = Column(Integer)
    rating = Column(Float)
    description = Column(Text)
    language = Column(String)
    country = Column(String)
    box_office = Column(Float)

    genres = relationship("Genre", secondary=movie_genre_table, back_populates="movies")
    people = relationship("Person", secondary=movie_person_role_table, back_populates="movies")
    companies = relationship("ProductionCompany", secondary=movie_company_table, back_populates="movies")
    keywords = relationship("Keyword", secondary=movie_keyword_table, back_populates="movies")
    reviews = relationship("Review", back_populates="movie")
    awards = relationship("Award", back_populates="movie")

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birthdate = Column(Date)
    nationality = Column(String)
    gender = Column(String)
    bio = Column(Text)

    movies = relationship("Movie", secondary=movie_person_role_table, back_populates="people")

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    movies = relationship("Movie", secondary=movie_genre_table, back_populates="genres")

class ProductionCompany(Base):
    __tablename__ = 'production_companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    founded_date = Column(Date)

    movies = relationship("Movie", secondary=movie_company_table, back_populates="companies")

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    reviewer_name = Column(String)
    rating = Column(Float)
    comment = Column(Text)
    review_date = Column(Date)

    movie = relationship("Movie", back_populates="reviews")

class Award(Base):
    __tablename__ = 'awards'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    award_name = Column(String)
    category = Column(String)
    year = Column(Integer)
    won = Column(Boolean)

    movie = relationship("Movie", back_populates="awards")

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, unique=True)

    movies = relationship("Movie", secondary=movie_keyword_table, back_populates="keywords")


