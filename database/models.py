from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship 


Base = declarative_base()


class Person(Base):

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(length=40), nullable=False)
    last_name = Column(String(length=40), nullable=False)

    favourite = relationship("Favorite", back_populates="person")
    blacklist = relationship("BlackList", back_populates="person")
    photo = relationship("Photo", back_populates="person")


class Photo(Base):

    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
    url = Column(String(length=200), unique=True, nullable=False)

    person = relationship(Person, back_populates="photo")


class Favourite(Base):

    __tablename__ = 'favourite'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), unique=True, nullable=False)

    person = relationship(Person, back_populates="favourite")

class BlackList(Base):

    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.id"), unique=True, nullable=False)

    person = relationship(Person, back_populates="blacklist")

def create_tables(engine):
    Base.metadata.create_all(engine)