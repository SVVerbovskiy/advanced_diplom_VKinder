from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(length=40), nullable=False)
    last_name = Column(String(length=40), nullable=False)


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)

    user = relationship(User, backref="photo")


class Favourite(Base):
    __tablename__ = "favourite"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)


class BlackList(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)


def create_tables(engine):
    '''Создание таблиц в базе данных.'''
    Base.metadata.create_all(engine)

def drop_tables(engine):
    '''Удаление таблиц в базе данных.'''
    Base.metadata.drop_all(bind=engine, tables=[User.__table__, Photo.__table__])