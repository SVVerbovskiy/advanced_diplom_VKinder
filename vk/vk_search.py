import requests
from config import vk_token


class VkClient:
    url = "https://api.vk.com/method/"

    def __init__(self, token: str):
        self.token = token

    def search_users(self, offset: str, count: str, hometown: str, sex: str, age: str):
        '''Поиск пользователей по определённым критериям.'''
        url = self.url + "users.search"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "sort": "0",
            "offset": offset,
            "count": count,
            "hometown": hometown,
            "sex": sex,
            "age_from": age,
            "age_to": age,
            "has_photo": "1",
        }

        response = requests.get(url=url, params=params)
        if response.ok:
            if "error" not in response.json():
                return [_ for _ in response.json()["response"]["items"]]
        else:
            return None

    # def get_profile_photos(self, owner_id: str):
    #     '''Получение фотографий профиля пользователя.'''
    #     url = self.url + "photos.get"
    #     params = {
    #         "access_token": self.token,
    #         "v": "5.131",
    #         "owner_id": owner_id,
    #         "album_id": "profile",
    #         "extended": "1",
    #         "photo_sizes": "1",
    #     }
    #
    #     response = requests.get(url=url, params=params)
    #     if response.ok:
    #         if "error" not in response.json():
    #             return response.json()["response"]["items"]
    #     else:
    #         return None

    def get_all_photos(self, owner_id: str):
        '''Получение всех фотографий пользователя.'''
        url = self.url + "photos.getAll"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "owner_id": owner_id,
            "album_id": "profile",
            "extended": "1",
            "photo_sizes": "1",
            "no_service_albums": "0"
        }

        response = requests.get(url=url, params=params)
        if response.ok:
            if "error" not in response.json():
                return response.json()["response"]["items"]
        else:
            return None


def get_three_popular_profile_photos(profile_photos: list):
    '''Получение трёх самых популярных фотографий пользователя.'''
    if len(profile_photos) >= 3:
        likes = []
        popular_profile_photos = []

        for photo in profile_photos:
            likes.append(photo["likes"]["count"])
        likes = list(set(likes))
        likes.sort(reverse=True)
        likes = likes[:3]

        for item in likes:
            for photo in profile_photos:
                if photo["likes"]["count"] == item:
                    popular_profile_photos.append(photo)

        return popular_profile_photos[:3]

    else:
        return None


def get_potential_friends(client: VkClient, sex: str, hometown: str, age: str):
    '''Поиск пользователей по заданным параметрам.'''
    if int(sex) == 1:
        desired_sex = "2"
    else:
        desired_sex = "1"

    potential_friends = client.search_users(
        offset="0", count="1000", hometown=hometown, sex=desired_sex, age=age
    )

    return potential_friends


def get_potential_friend_photos(client: VkClient, owner_id: str):
    '''Получение фотографий пользователя.'''
    photos = client.get_all_photos(owner_id=owner_id)
    if photos is None or len(photos) < 3:
        return None

    popular_photos = get_three_popular_profile_photos(photos)

    return [_["sizes"][-1]["url"] for _ in popular_photos]


if __name__ == "__main__":
    '''Пример работы.'''

    # Создаём экземпляр класса vk клиента
    vk_client = VkClient(vk_token)

    # Ищем потенциальных друзей по критериям
    my_potential_friends = get_potential_friends(client=vk_client, sex="2", hometown="Москва", age="20")
    print(my_potential_friends)

    # Получаем три популярные фотографии по id пользователя
    my_potential_friend_photos = get_potential_friend_photos(client=vk_client, owner_id="481468488")
    print(my_potential_friend_photos)
