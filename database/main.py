import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables
from db_config import DSN

engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

session.close()