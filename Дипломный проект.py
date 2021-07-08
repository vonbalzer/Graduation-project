import requests
import json

def get_dict_vk(id_user_vk, token_vk):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': f'{id_user_vk}',
        'album_id': 'profile',
        'extended': '1',
        'access_token': f'{token_vk}',
        'v':'5.131',
    }
    res = requests.get(URL, params=params)
    return res.json()

def creat_folder(id_user_vk, def_token_ya):

        url_yandex_disk_creat_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Connect-type': 'application/json', 'Authorization': f'{def_token_ya}'}
        params = {"path": f'{id_user_vk}'}
        res_ya = requests.put(url_yandex_disk_creat_folder, headers=headers, params=params)

        if '409' in str(res_ya) or '201' in str(res_ya):
            return f'На YandexDisk создана папка с именем :{id_user_vk}'
        elif '401' in str(res_ya):
            return f'Указанный токен YandexDisk неверный' \
                   f' или не предоставляет достаточных прав для заливки фотографий.'
        else:
            return f'Ошибка: {str(res_ya)} ==> {res_ya.json()["message"]}'

def upload_foto(def_dict_vk, def_id_user, def_token_ya):
    counter = 0
    max_foto = 0
    best_url: str
    size_url = []
    list_likes = []
    size_foto: str
    list_foto = []
    dict_foto = {}
    len_foto = 0

    if 'error' in str(def_dict_vk):
        print()
        print(def_dict_vk['error']['error_msg'])

    if 'response' in str(def_dict_vk):

        for key in def_dict_vk['response']['items']:
            def_dict_vk['response']['items'][len_foto]['likes']
            len_foto += 1

        url_yandexdisk_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Connect-type': 'application/json', 'Authorization': f'{def_token_ya}'}
        print()
        print(f'Скачиваем фото из профиля VK: {def_id_user}')
        print("-------------------------------------")
        print(f'Будет загружено {len_foto} фото:')

        for keys in def_dict_vk['response']['items']:
            xp = def_dict_vk['response']['items'][counter]['sizes']
            size_url.append(xp)
            for val in size_url:
                for key in val:
                    if int(key['height']) > int(max_foto):
                        max_foto = key['height']
                    best_url = key['url']
                    size_foto = key['type']
            url = best_url

            list_likes.append(def_dict_vk['response']['items'][counter]['likes']['count'])
            params = {"path": f'{def_id_user}/{list_likes[counter]}', "url": url, "overwrite": "true"}
            requests.post(url_yandexdisk_upload, headers=headers, params=params)

            dict_foto["file_name"] = f'{list_likes[counter]}.jpg'
            dict_foto["size"] = size_foto
            list_foto.append(dict_foto)
            print(f'Фото "{list_likes[counter]}.jpg" отпралено на YandexDisk.\n'
                  f'Фото {counter + 1} из {len_foto} ')

            counter += 1
        print()
        print(f'==>> Загрузка фото на YandexDisk завершена!')

        with open('log.txt', "a") as file:
            file.write(json.dumps(list_foto, sort_keys=True, indent=4))

print("***********************************************")
id_user = str(input("Введите id пользователя VK: "))
token_vk = str(input("Введите токен API VK: "))
token_ya = str(input("Введите токен API YandexDisk: "))
print("***********************************************")

dict_vk = get_dict_vk(id_user, token_vk)
print(creat_folder(id_user, token_ya))
upload_foto(dict_vk, id_user, token_ya)