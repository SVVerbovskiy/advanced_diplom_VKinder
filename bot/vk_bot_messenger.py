import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randrange
from config import api_group_key

vk_auth = vk_api.VkApi(token=api_group_key)
vk = vk_auth.get_api()
longpoll = VkLongPoll(vk_auth)

favour = []
users_requests = dict()
client_match = dict()


def send_msg(user_id, message, keyboard=None):
    text = {
        'user_id': user_id,
        'message': message,
        'random_id': randrange(10 ** 7)
    }

    if keyboard is not None:
        text['keyboard'] = keyboard.get_keyboard()

    vk_auth.method('messages.send', text)


def get_start(user_id):
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
    send_msg(user_id, f'Всего доброго! До скорых встреч!')


def get_city(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'В каком городе будем искать?', keyboard)


def confirm_city(user_id, city):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Все верно', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Изменить', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Ищем в городе {city.title()}?', keyboard)


def get_sex(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Парня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Девушку', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', color=VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Кого будем искать?', keyboard)


def get_age_from(user_id):
    send_msg(user_id, f'Со скольки лет?')


def get_age_to(user_id):
    send_msg(user_id, 'До скольки лет?')


def confirm_data(user_id, city, sex, age_from, age_to):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Всё верно', VkKeyboardColor.SECONDARY)
    keyboard.add_button('Изменить параметры', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, f'Ищем {sex} в возрасте от {age_from} до {age_to} из города {city.title()}?', keyboard)


def change_data(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Город', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Пол', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Возраст', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Что хотите изменить?', keyboard)


def send_photo(user_id, url):
    vk.messages.send(user_id=user_id, attachment=url, random_id=randrange(10**7))


def send_person():
    pass


def add_to_favorite():
    favour.append()
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Дальше', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить общение :(', VkKeyboardColor.NEGATIVE)
    send_msg(id, f'"ИМЯ" в избранном!', keyboard)


def list_is_over(user_id):
    send_msg(user_id, 'По данному запросу ничего больше нет(')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('ИЗБРАННОЕ', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Начнём подбор!', VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Завершить', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Начнём новый подбор?', keyboard)


def show_favorite(user_id):
    pass


flag = ''
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.message.lower()
        client_id = event.user_id
        if msg and flag == '':
            get_start(client_id)
            flag = 'start'
        if msg == 'завершить':
            param = f'"city": "{users_requests[client_id]["city"]}", ' \
                    f'"sex": "{users_requests[client_id]["sex"]}", ' \
                    f'"age_from": "{users_requests[client_id]["age_from"]}", ' \
                    f'"age_to": "{users_requests[client_id]["age_to"]}"'
            write_count(client_id, count, param)
            get_finish(client_id)
            flag = ''
        elif msg == 'начнём подбор!':
            users_requests[client_id] = {"city": "", "sex": "", "age_from": "", "age_to": "", "token": ""}
            get_city(client_id)
            flag = 'to_city'
        elif flag == 'to_city':
            confirm_city(client_id, msg)
            flag = msg
        elif msg == 'все верно' and flag != 'confirm data':
            city = flag
            users_requests[client_id]["city"] = city
            flag = 'to_sex'
            get_sex(client_id)
        elif msg == 'изменить город':
            get_city(client_id)
            if users_requests[client_id]["sex"] == "":
                flag = 'to_city'
            else:
                flag = 'change city'
        elif msg == 'парня' and flag != 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 2
            get_age_from(client_id)
            flag = 'to_age_from'
        elif msg == 'девушку' and flag != 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 1
            get_age_from(client_id)
            flag = 'to_age_from'
        elif flag == 'to_age_from':
            try:
                age_f = int(msg.strip())
                users_requests[client_id]["age_from"] = age_f
                get_age_to(client_id)
                flag = 'to_age_to'
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif flag == 'to_age_to':
            try:
                age_t = int(msg.strip())
                users_requests[client_id]["age_to"] = age_t
                flag = 'confirm'
                confirm_data(user_id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
            except ValueError:
                send_msg(client_id, 'Что-то пошло не так')
                get_age_from(client_id)
        elif msg == 'изменить параметры':
            change_data(client_id)
        elif msg == 'город':
            get_city(client_id)
            flag = 'change city'
        elif flag == 'change city':
            flag = 'confirm data'
            new_city = msg
            confirm_city(client_id, msg)
        elif msg == 'да, город верный' and flag == 'confirm data':
            city = new_city
            users_requests[client_id]["city"] = city
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'возраст':
            get_age_from(client_id)
            flag = 'to_age_from'
        elif msg == 'пол':
            flag = 'change sex'
            get_sex(client_id)
        elif msg == 'парня' and flag == 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 2
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'девушку' and flag == 'change sex':
            sex = msg
            users_requests[client_id]["sex"] = 1
            confirm_data(id=client_id, city=city, sex=sex, age_from=age_f, age_to=age_t)
        elif msg == 'давай смотреть!':
            count = 0
            param = f'{{"city": "{users_requests[client_id]["city"]}", "sex": "{users_requests[client_id]["sex"]}", '
            param += f'"age_from": "{users_requests[client_id]["age_from"]}", "age_to": '
            param += f'"{users_requests[client_id]["age_to"]}", "token": "{users_requests[client_id]["token"]}"}}'
            write_count(client_id, count, param)
            current_match = client_match[client_id][count]
            if users_requests[client_id]["token"]:
                token = users_requests[client_id]["token"]
            else:
                token = api_group_key
            user_info = send_person(client_id, current_match, token)
        elif msg == 'дальше':
            count += 1
            if count < match_count:
                current_match = client_match[client_id][count]
                user_info = send_person(client_id, current_match, token)
            else:
                list_is_over(client_id)
        elif msg == 'в избранное':
            add_to_favorite(id=client_id, user_info=user_info)
        elif msg == 'избранное':
            show_favorite(client_id)

