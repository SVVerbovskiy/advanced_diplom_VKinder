from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship 


Base = declarative_base()


class User(Base):

    __tablename__ = 'user' 

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(length=40), nullable=False)
    last_name = Column(String(length=40), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(length=10), nullable=False)
    hometown = Column(String(length=40), nullable=False)

    favorite = relationship("Favorite", back_populates="user")


class Person(Base):

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(length=40), nullable=False)
    last_name = Column(String(length=40), nullable=False)

    photo = relationship("Photo", back_populates="person")
    favorite = relationship("Favorite", back_populates="person")


class Photo(Base):

    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    url = Column(String(length=200), unique=True, nullable=False)

    person = relationship(Person, back_populates="photo")


class Favorite(Base):

    __tablename__ = 'favorite'

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), primary_key=True)

    user = relationship(User, back_populates="favorite")
    person = relationship(Person, back_populates="favorite")


def create_tables(engine):
    Base.metadata.create_all(engine)