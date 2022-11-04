import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, User, Photo, Favourite, BlackList
from db_config import DSN


def create_connection():
    engine = sq.create_engine(DSN)
    return engine


class Vkinder:
    def __init__(self):
        self.engine = create_connection()
        session = sessionmaker(bind=self.engine)
        self.session = session()
        create_tables(self.engine)

    def session_close(self):
        self.session.close()

    def add_user_data(self, data: list):
        for record in data:
            self.session.add(
                User(
                    user_id=record["id"],
                    first_name=record["first_name"],
                    last_name=record["last_name"],
                )
            )
        self.session.commit()

    def get_user(self, id: int):
        return self.session.query(User).filter(User.id == id).first()

    def add_photo_urls(self, user_id: int, urls: list):
        for url in urls:
            self.session.add(
                Photo(
                    user_id=user_id,
                    url=url,
                )
            )
        self.session.commit()

    def get_photo_urls(self, user_id: int):
        return self.session.query(Photo).filter(Photo.user_id == user_id).all()

    def add_to_favourite(self, user_id: int):
        self.session.add(
            Favourite(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_favourite(self, user_id: int):
        if (
            self.session.query(Favourite)
            .filter(Favourite.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def get_favourite(self):
        return self.session.query(Favourite).all()

    def add_to_blacklist(self, user_id: int):
        self.session.add(
            BlackList(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_blacklist(self, user_id: int):
        if (
            self.session.query(BlackList)
            .filter(BlackList.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True