import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from database.models import create_tables, drop_tables, User, Photo, Favourite, BlackList
from database.db_config import DSN


def create_connection():
    engine = sq.create_engine(DSN)
    return engine


class Vkinder:
    def __init__(self):
        self.engine = create_connection()
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def create_new_tables(self):
        """Добавление новых таблиц"""
        create_tables(self.engine)

    def drop_old_tables(self):
        """Удаление заполненных таблиц"""
        drop_tables(self.engine)

    def add_user_data(self, data: list):
        """Добавление информации о пользователе в базу данных"""
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
        """Получение пользователя из базы данных"""
        return self.session.query(User).filter(User.id == id).first()

    def user_search(self, user_id: int):
        """Поиск пользователя в таблице User по user_id"""
        return self.session.query(User).filter(User.user_id == user_id).first()

    def get_all_user(self):
        """Получение всех пользователей из базы данных"""
        return self.session.query(User).all()

    def add_photo_urls(self, user_id: int, urls: list):
        """Добавление фотографии в базу данных"""
        for url in urls:
            self.session.add(
                Photo(
                    user_id=user_id,
                    url=url,
                )
            )
        self.session.commit()

    def get_photo_urls(self, user_id: int):
        """Получение фотографий из базы данных"""
        return self.session.query(Photo).filter(Photo.user_id == user_id).all()

    def add_to_favourite(self, user_id: int):
        """Добавление пользователя в таблицу Favourite"""
        self.session.add(
            Favourite(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_favourite(self, user_id: int):
        """Проверка на наличие пользователя в таблице Favourite"""
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
        """Получение всех пользователей, добавленных в Favourite"""
        return self.session.query(Favourite).all()

    def add_to_blacklist(self, user_id: int):
        """Добавление пользователя в чёрный список"""
        self.session.add(
            BlackList(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_blacklist(self, user_id: int):
        """Проверка на наличие пользователя в чёрном списке"""
        if (
            self.session.query(BlackList)
            .filter(BlackList.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True


#if __name__ == "__main__":
#    """Пример работы."""
#    from fixtures import users, urls
#
#    # Создаём класс для работы с БД
#    vkinder = Vkinder()
#    vkinder.drop_old_tables()
#    vkinder.create_new_tables()
#   
#    # Записываем данные о пользователях, полученных через vk_search, в базу данных в таблицу User
#    # На вход подаётся список, см. fixtures.users
#    vkinder.add_user_data(data=users)
#
#    # Получаем данные о пользователе по его порядковому номеру из базы User, порядковые номера начинаются с 1,
#    # далее 2, 3 и т.д.
#    user1 = vkinder.get_user(id=1)
#    # Вот так обращаемся к результату запроса
#    print("vkinder.get_user:", user1.id, user1.user_id, user1.first_name, user1.last_name)
#
#    # Записываем url фото для пользователя в базу данных в таблицу Photo. Url получаем через vk_search
#    # На вход подаётся список, см. fixtures.urls
#    vkinder.add_photo_urls(user_id=537894429, urls=urls)
#
#    # Получаем url фото из базы для пользователя через user_id
#    user_urls = vkinder.get_photo_urls(user_id=537894429)
#    # Вот так обращаемся к результату запроса
#    for url in user_urls:
#        print("vkinder.get_photo_urls:", url.user_id, url.url)
#
#    # Добавляем пользователя в таблицу Favourite по его user_id
#    vkinder.add_to_favourite(user_id=679335476)
#
#    # Проверяем, есть ли пользователь в избранном по его user_id
#    result1 = vkinder.check_favourite(user_id=679335476)
#    result2 = vkinder.check_favourite(user_id=679335479)
#    print("vkinder.check_favourite:", result1)
#    print("vkinder.check_favourite:", result2)
#
#    # Получаем список пользователей из избранного
#    favorites = vkinder.get_favourite()
#    print(len(favorites))
#    for favorite in favorites:
#        print("vkinder.get_favourite:", favorite.user_id)
#
#    # Добавляем пользователя в таблицу Blacklist по его user_id
#    vkinder.add_to_blacklist(user_id=431194792)
#
#    # Проверяем, есть ли пользователь в чёрном списке по его user_id
#    result3 = vkinder.check_blacklist(user_id=431194792)
#    result4 = vkinder.check_blacklist(user_id=431194791)
#    print("vkinder.check_blacklist:", result3)
#    print("vkinder.check_blacklist:", result4)