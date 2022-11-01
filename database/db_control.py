import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Person, Photo, Favourite, BlackList
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

    def add_person_data(self, data: list):
        for record in data:
            self.session.add(
                Person(
                    vk_id=record["id"],
                    first_name=record["first_name"],
                    last_name=record["last_name"],
                )
            )
        self.session.commit()

    def get_person(self, person_id: int):
        return self.session.query(Person).filter(Person.id == person_id).first()

    def add_photo_urls(self, person_id: int, urls: list):
        for url in urls:
            self.session.add(
                Photo(
                    person_id=person_id,
                    url=url,
                )
            )
        self.session.commit()

    def get_photo_urls(self, person_id: int):
        return self.session.query(Photo).filter(Photo.person_id == person_id).all()

    def add_to_favourite(self, person_id: int):
        self.session.add(
            Favourite(
                person_id=person_id,
            )
        )
        self.session.commit()

    def check_favourite(self, person_id: int):
        if (
            self.session.query(Favourite)
            .filter(Favourite.person_id == person_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def get_favourite(self):
        return self.session.query(Favourite).all()

    def add_to_blacklist(self, person_id: int):
        self.session.add(
            BlackList(
                person_id=person_id,
            )
        )
        self.session.commit()

    def check_blacklist(self, person_id: int):
        if (
            self.session.query(BlackList)
            .filter(BlackList.person_id == person_id)
            .first()
            is None
        ):
            return False
        else:
            return True


vkinder = Vkinder()
# print(vkinder)
