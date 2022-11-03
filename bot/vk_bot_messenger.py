import requests
import vk_api
from io import BytesIO
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
from config import api_group_key, vk_token
from vk.vk_search import get_potential_friends, get_potential_friend_photos, VkClient

vk_auth = vk_api.VkApi(token=api_group_key)
vk = vk_auth.get_api()
longpoll = VkLongPoll(vk_auth)
upload = VkUpload(vk_auth)
vk_client = VkClient(vk_token)

favour = []
users_requests = {}


def send_msg(user_id, message, keyboard=None):
    """
    Функция отправляет сообщение собеседнику

    :param user_id: id собеседника
    :type user_id: int
    :param message: текст сообщения
    :type : str
    :param keyboard: клавиатура с необходимыми кнопками
    :type : class instance 'vk_api.keyboard.VkKeyboard'
    """
    text = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    }

    if keyboard is not None:
        text['keyboard'] = keyboard.get_keyboard()

    vk_auth.method('messages.send', text)


def get_start(user_id):
    """
    Функция отправляет кнопку предлагающую начать подбор

    :param user_id: id собеседника
    :type user_id: int
    """
    # Тут в начало добавить ссылку на избранное из бд и потом в if проверять длину БД. Если >0
    if len(favour) > 0:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.POSITIVE)
        keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
        send_msg(user_id, f'Привет!', keyboard)
    else:
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Начнём подбор!', VkKeyboardColor.PRIMARY)
        send_msg(user_id, f'Привет', keyboard)


def get_finish(user_id):
    """
    Функция отправляет сообщение при завершении сеанса общения

    :param user_id: id собеседника
    :type user_id: int
    """
    send_msg(user_id, f'Всего доброго! До скорых встреч!')


def get_hometown(user_id):
    """
    Функция отправляет сообщение с просьбой ввести город в котором будем искать

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'В каком городе будем искать?', keyboard)


def confirm_hometown(user_id, hometown):
    """
    Функция отправляет кнопки для изменения и подтверждения города

    :param user_id: id собеседника
    :type user_id: int
    :param hometown: название города которое ввёл собеседник
    :type hometown: str
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Да, город верный', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Изменить город', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Ищем в городе {hometown.capitalize()}?', keyboard)


def get_sex(user_id):
    """
    Функция отправляет кнопки для выбора пола партнёра

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Парня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Девушку', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Кого будем искать?', keyboard)


def get_age(user_id):
    """
    Функция отправляет сообщение с запросом возраста для поиска партнера

    :param user_id: id собеседника
    :type user_id: int
    """
    send_msg(user_id, f'Укажите возраст:')


def confirm_data(user_id, sex, hometown, age):
    """
    Функция отправляет кнопки для изменения и подтверждения параметров поиска

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
    keyboard.add_button('Все верно', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Изменить параметры', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Ищем {sex} в возрасте {age} из города {hometown.capitalize()}?', keyboard)


def change_data(user_id):
    """
    Функция отправляет кнопки для выбора параметра который необходимо изменить

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Город', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Пол', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Возраст', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Что хотите изменить?', keyboard)


def send_match(user_id):
    """
    Функция отправляет сообщение с количеством совпадений и кнопку для начала просмотра

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Давай смотреть!', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'По вашему запросу найдено {len(friends_list())} пользователей!', keyboard)


def send_photo(user_id, url):
    """
    Функция отправляет фотографию

    :param user_id: id собеседника
    :type user_id: int
    :param url: вложение
    :type url: str
    """
    vk.messages.send(user_id=user_id, attachment=url, random_id=randrange(10 ** 7))


def send_next(user_id):
    """
    Функция отправляет навигационные кнопки для просмотра информации о следующем пользователе,
    добавлении его в список избранного или в черный список

    :param user_id: id собеседника
    :type user_id: int
    """
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('В чёрный список', VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('В избранное', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Что думаете о данном пользователе?', keyboard)


def add_to_favorite(user_id):
    """
    Функция добавляет партнера в избранное и записывает в БД

    :param user_id: id собеседника
    :type user_id: int
    """
    # тут прописать добавление в избранное в базу данных

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'"ИМЯ" в избранном!', keyboard)


def list_is_over(user_id):
    """
    Функция отправляет сообщение о том что список совпадений закончился и навигационные кнопки

    :param user_id: id собеседника
    :type user_id: int
    """
    send_msg(user_id, 'По данному запросу ничего больше нет(')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Начнём подбор!', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Начнём новый подбор?', keyboard)


def show_favorite(user_id):
    """
    Функция отправляет сообщения с данными о списке избранных получив данные из БД

    :param user_id: id собеседника
    :type user_id: int
    """
    # В данной функции дописать список избранного из БД и вывести его длину
    send_msg(user_id, f'У Вас в избранном {len(favour)} человек:')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Смотрим дальше?', keyboard)


def add_to_blacklist(user_id):
    """
    Функция добавляет пользователя в черный список и делает запись в БД

    :param user_id: id собеседника
    :type user_id: int
    """
    #     тут дописать механизм добавления в черный список
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Пользователь добавлен в чёрный список и больше не будет появляться в выдаче!', keyboard)


def friends_list():
    """
    Функция формирует список возможных друзей используя данные полученные после общения с пользователем
    """
    friends = get_potential_friends(client=vk_client,
                                    sex=users_requests['sex'],
                                    hometown=users_requests['hometown'],
                                    age=users_requests['age'])
    return friends


def main():
    flag = ''
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.message.lower()
            client_id = event.user_id
            if msg and flag == '':
                get_start(client_id)
                flag = 'start'
            if msg == 'завершить':
                get_finish(client_id)
                flag = ''
            elif msg == 'начнём подбор!':
                get_hometown(client_id)
                flag = 'to_hometown'
            elif flag == 'to_hometown':
                confirm_hometown(client_id, msg)
                flag = msg
            elif msg == 'да, город верный' and flag != 'confirm data':
                hometown = flag
                users_requests["hometown"] = hometown.capitalize()
                flag = 'to_sex'
                get_sex(client_id)
            elif msg == 'изменить город':
                get_hometown(client_id)
                if users_requests["sex"] == "":
                    flag = 'to_hometown'
                else:
                    flag = 'change hometown'
            elif msg == 'парня' and flag != 'change sex':
                sex = msg
                users_requests["sex"] = '2'
                get_age(client_id)
                flag = 'to_age'
            elif msg == 'девушку' and flag != 'change sex':
                sex = msg
                users_requests["sex"] = '1'
                get_age(client_id)
                flag = 'to_age'
            elif flag == 'to_age':
                try:
                    age = msg.strip()
                    users_requests["age"] = age
                    flag = 'confirm'
                    confirm_data(user_id=client_id, sex=sex, hometown=users_requests['hometown'],
                                 age=users_requests['age'])
                except ValueError:
                    send_msg(client_id, 'Что-то пошло не так')
                    get_age(client_id)
            elif msg == 'изменить параметры':
                change_data(client_id)
            elif msg == 'город':
                get_hometown(client_id)
                flag = 'change hometown'
            elif flag == 'change hometown':
                flag = 'confirm data'
                new_hometown = msg
                confirm_hometown(client_id, msg)
            elif msg == 'да, город верный' and flag == 'confirm data':
                hometown = new_hometown
                users_requests["hometown"] = hometown.capitalize()
                confirm_data(user_id=client_id, sex=sex, hometown=users_requests['hometown'],
                             age=users_requests['age'])
            elif msg == 'возраст':
                get_age(client_id)
                flag = 'to_age'
            elif msg == 'пол':
                flag = 'change sex'
                get_sex(client_id)
            elif msg == 'парня' and flag == 'change sex':
                sex = msg
                users_requests["sex"] = '1'
                confirm_data(user_id=client_id, sex=sex, hometown=users_requests['hometown'],
                             age=users_requests['age'])
            elif msg == 'девушку' and flag == 'change sex':
                sex = msg
                users_requests["sex"] = '2'
                confirm_data(user_id=client_id, sex=sex, hometown=users_requests['hometown'],
                             age=users_requests['age'])
            elif msg == 'все верно':
                send_match(client_id)
                friends = friends_list()
            elif msg == 'давай смотреть!' or msg == 'дальше':
                pops = friends.pop()
                full_name = f"{pops['first_name']} {pops['last_name']}"
                page_link = f"https://vk.com/id{pops['id']}"
                photo_list = get_potential_friend_photos(client=vk_client, owner_id=f"{pops['id']}")
                send_msg(client_id, full_name)
                send_msg(client_id, page_link)
                if photo_list is None:
                    send_msg(client_id, 'У пользователя недостаточно фотографий')
                else:
                    for photo in photo_list:
                        img = requests.get(photo).content
                        f = BytesIO(img)
                        upload_photo = upload.photo_messages(f)[0]
                        url = ('photo{}_{}'.format(upload_photo['owner_id'], upload_photo['id']))
                        send_photo(client_id, url=url)
                send_next(client_id)
            elif msg == 'в избранное':
                add_to_favorite(user_id=client_id)
            elif msg == 'избранное':
                show_favorite(client_id)
            elif msg == 'в чёрный список':
                add_to_blacklist(client_id)


if __name__ == '__main__':
    main()
