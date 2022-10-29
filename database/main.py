import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables
from db_config import DSN


def create_connection():
    engine = sq.create_engine(DSN)
    return engine 

class Vkinder:

    def __init__(self):
        self.engine = create_connection()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_tables(self.engine)

    def session_close(self):
        self.session.close()




vkinder = Vkinder()
print(vkinder)