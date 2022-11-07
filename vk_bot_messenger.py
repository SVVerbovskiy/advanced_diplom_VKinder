import requests
import vk_api
from io import BytesIO
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
from config import api_group_key, vk_token
from vk.vk_search import get_potential_friends, get_potential_friend_photos, VkClient
from database.db_control import Vkinder

vk_auth = vk_api.VkApi(token=api_group_key)
vk = vk_auth.get_api()
longpoll = VkLongPoll(vk_auth)
upload = VkUpload(vk_auth)
vk_client = VkClient(vk_token)
vkinder = Vkinder()
vkinder.drop_old_tables()
vkinder.create_new_tables()

users_requests = {"hometown": "", "sex": "", "age": ""}


def send_msg(user_id, message, keyboard=None):
    """
    Отправка сообщения собеседнику

    :param user_id: id собеседника
    :type user_id: int
    :param message: текст сообщения
    :type : str
    :param keyboard: клавиатура с необходимыми кнопками
    :type : class instance 'vk_api.keyboard.VkKeyboard'
    """
    text = {"user_id": user_id, "message": message, "random_id": randrange(10**7)}

    if keyboard is not None:
        text["keyboard"] = keyboard.get_keyboard()

    vk_auth.method("messages.send", text)


def get_start(user_id):
    """
    Отправка кнопки, предлагающей начать подбор

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Начнём подбор!", VkKeyboardColor.PRIMARY)
    send_msg(user_id, f"Привет", keyboard)


def get_finish(user_id):
    """
    Отправка сообщения при завершении сеанса общения

    :param user_id: id собеседника
    :type user_id: int
    """

    send_msg(user_id, f"Всего доброго! До скорых встреч!")


def get_hometown(user_id):
    """
    Отправка сообщения с просьбой ввести город, по которому будет осуществляться поиск

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, "В каком городе будем искать?", keyboard)


def confirm_hometown(user_id, hometown):
    """
    Отправка кнопок для изменения и подтверждения города

    :param user_id: id собеседника
    :type user_id: int
    :param hometown: название города, которое ввёл собеседник
    :type hometown: str
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Да, город верный", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Изменить город", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f"Ищем в городе {hometown.capitalize()}?", keyboard)


def get_sex(user_id):
    """
    Отправка кнопки для выбора пола партнёра

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Парня", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("Девушку", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f"Кого будем искать?", keyboard)


def get_age(user_id):
    """
    Отправка сообщения с запросом возраста для поиска партнёра

    :param user_id: id собеседника
    :type user_id: int
    """
    send_msg(user_id, f"Укажите возраст:")


def confirm_data(user_id, sex, hometown, age):
    """
    Отправка кнопок для изменения и подтверждения параметров поиска

    :param user_id: id собеседника
    :type user_id: int
    :param sex: пол партнёра
    :type sex: str
    :param hometown: название города
    :type hometown: str
    :param age: нижняя планка возраста
    :type age: str
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Все верно", VkKeyboardColor.SECONDARY)
    keyboard.add_button("Изменить параметры", VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_msg(
        user_id,
        f"Ищем {sex} в возрасте {age} из города {hometown.capitalize()}?",
        keyboard,
    )


def change_data(user_id):
    """
    Отправка кнопок для выбора параметра, который необходимо изменить

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Город", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Пол", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Возраст", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_msg(user_id, "Что хотите изменить?", keyboard)


def send_match(user_id):
    """
    Отправка сообщения с количеством совпадений и кнопки для начала просмотра

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Давай смотреть!", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_msg(
        user_id,
        f"По вашему запросу найдено {len(vkinder.get_all_user())} пользователей!",
        keyboard,
    )


def send_photo(user_id, url):
    """
    Отправка фотографии

    :param user_id: id собеседника
    :type user_id: int
    :param url: вложение
    :type url: str
    """
    vk.messages.send(user_id=user_id, attachment=url, random_id=randrange(10**7))


def send_next(user_id):
    """
    Отправка навигационных кнопок для просмотра информации о следующем пользователе,
    добавлении его в список избранного или в чёрный список

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("В чёрный список", VkKeyboardColor.NEGATIVE)
    keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("ИЗБРАННОЕ", VkKeyboardColor.PRIMARY)
    keyboard.add_button("В избранное", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f"Что думаете о данном пользователе?", keyboard)


def add_to_blacklist(user_id):
    """
    Добавление пользователя в чёрный список и создание соответствующей записи в базе данных

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("ИЗБРАННОЕ", VkKeyboardColor.PRIMARY)
    keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f"Пользователь добавлен в чёрный список", keyboard)


def friends_list():
    """
    Формирование списка возможных друзей, используя данные, полученные после общения с пользователем
    """
    friends = get_potential_friends(
        client=vk_client,
        sex=users_requests["sex"],
        hometown=users_requests["hometown"],
        age=users_requests["age"],
    )
    return friends


def main():
    flag = ""
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.message.lower()
            client_id = event.user_id
            if msg and flag == "":
                get_start(client_id)
                flag = "start"
            if msg == "завершить":
                get_finish(client_id)
                flag = ""
            elif msg == "начнём подбор!":
                vkinder.drop_old_tables()
                vkinder.create_new_tables()
                get_hometown(client_id)
                flag = "to_hometown"
            elif flag == "to_hometown":
                confirm_hometown(client_id, msg)
                flag = msg
            elif msg == "да, город верный" and flag != "confirm data":
                hometown = flag
                users_requests["hometown"] = hometown.capitalize()
                flag = "to_sex"
                get_sex(client_id)
            elif msg == "изменить город":
                get_hometown(client_id)
                if users_requests["sex"] == "":
                    flag = "to_hometown"
                else:
                    flag = "change hometown"
            elif msg == "парня" and flag != "change sex":
                sex = msg
                users_requests["sex"] = "1"
                get_age(client_id)
                flag = "to_age"
            elif msg == "девушку" and flag != "change sex":
                sex = msg
                users_requests["sex"] = "2"
                get_age(client_id)
                flag = "to_age"
            elif flag == "to_age":
                try:
                    age = msg.strip()
                    users_requests["age"] = age
                    flag = "confirm"
                    confirm_data(
                        user_id=client_id,
                        sex=sex,
                        hometown=users_requests["hometown"],
                        age=users_requests["age"],
                    )
                except ValueError:
                    send_msg(client_id, "Что-то пошло не так")
                    get_age(client_id)
            elif msg == "изменить параметры":
                change_data(client_id)
            elif msg == "город":
                get_hometown(client_id)
                flag = "change hometown"
            elif flag == "change hometown":
                flag = "confirm data"
                new_hometown = msg
                confirm_hometown(client_id, msg)
            elif msg == "да, город верный" and flag == "confirm data":
                hometown = new_hometown
                users_requests["hometown"] = hometown.capitalize()
                confirm_data(
                    user_id=client_id,
                    hometown=users_requests["hometown"],
                    sex=users_requests["sex"],
                    age=users_requests["age"],
                )
            elif msg == "возраст":
                get_age(client_id)
                flag = "to_age"
            elif msg == "пол":
                flag = "change sex"
                get_sex(client_id)
            elif msg == "парня" and flag == "change sex":
                sex = msg
                users_requests["sex"] = "1"
                confirm_data(
                    user_id=client_id,
                    sex=sex,
                    hometown=users_requests["hometown"],
                    age=users_requests["age"],
                )
            elif msg == "девушку" and flag == "change sex":
                sex = msg
                users_requests["sex"] = "2"
                confirm_data(
                    user_id=client_id,
                    sex=sex,
                    hometown=users_requests["hometown"],
                    age=users_requests["age"],
                )
            elif msg == "все верно":
                vkinder.add_user_data(friends_list())
                send_match(client_id)
                count = 0
            elif msg == "давай смотреть!" or msg == "дальше":
                count += 1
                user = vkinder.get_user(id=count)
                full_name = f"{user.first_name} {user.last_name}"
                page_link = f"https://vk.com/id{user.user_id}"
                photo_list = get_potential_friend_photos(
                    vk_client, owner_id=user.user_id
                )
                if photo_list is not None:
                    vkinder.add_photo_urls(user.user_id, photo_list)
                    send_msg(client_id, full_name)
                    send_msg(client_id, page_link)
                    user_photos = vkinder.get_photo_urls(user.user_id)
                    for photo in user_photos:
                        img = requests.get(photo.url).content
                        f = BytesIO(img)
                        upload_photo = upload.photo_messages(f)[0]
                        url = "photo{}_{}".format(
                            upload_photo["owner_id"], upload_photo["id"]
                        )
                        send_photo(client_id, url=url)
                    send_next(client_id)
                else:
                    send_msg(client_id, full_name)
                    send_msg(client_id, page_link)
                    send_msg(
                        client_id,
                        "У пользователя недостаточно фото, можете перейти по ссылке на его страницу!",
                    )
                    send_next(client_id)
            elif msg == "в избранное":
                vkinder.add_to_favourite(user.user_id)
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("ИЗБРАННОЕ", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
                send_msg(
                    client_id,
                    f"Пользователь {full_name} {page_link} добавлен в избранное!",
                    keyboard,
                )
            elif msg == "избранное":
                favorites = vkinder.get_favourite()
                send_msg(client_id, f"У Вас в избранном {len(favorites)} человек:")
                for favorite in favorites:
                    user = vkinder.user_search(user_id=favorite.user_id)
                    full_name = f"{user.first_name} {user.last_name}"
                    page_link = f"https://vk.com/id{user.user_id}"
                    send_msg(client_id, f"{full_name} {page_link}")
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Дальше", VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button("Завершить", VkKeyboardColor.NEGATIVE)
                send_msg(client_id, "Смотрим дальше?", keyboard)
            elif msg == "в чёрный список":
                vkinder.add_to_blacklist(user.user_id)
                add_to_blacklist(client_id)


if __name__ == "__main__":
    main()
