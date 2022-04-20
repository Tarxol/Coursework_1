import requests
from datetime import datetime
import json
from tqdm import tqdm

token_vk = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
version = '5.131'
files_list = []
files_list_url = {}

class VkUser:

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token_vk,
            'v': version
        }

    def get_photo(self):
        photo_url = self.url + 'photos.get'
        photo_get_params = {
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'photo_sizes': 1
        }
        photo_lists = requests.get(photo_url, params={**self.params, **photo_get_params}).json()
        a = input(f'\nВведите кол-во скачиваемых фото(по умолчанию 5): ')
        if a.isnumeric() == False:
            quantity_photo = 5
        else:
            quantity_photo = int(a)
        photo_lists_info = []
        for photo in photo_lists['response']['items'][:quantity_photo]:
            info = {'file_name': str(photo['likes']['count']) +'.jpg',
                    'size': photo['sizes'][-1]['type']}
            info_1 = {'file_name': str(photo['likes']['count']) + '_' + str(datetime.fromtimestamp(photo['date']).date()) + '.jpg',
                    'size': photo['sizes'][-1]['type']}
            if info['file_name'] in files_list:
                files_list_url[info_1['file_name']] = photo['sizes'][-1]['url']
                photo_lists_info.append(info_1)
                files_list.append(info_1['file_name'])
            else:
                files_list_url[info['file_name']] = photo['sizes'][-1]['url']
                photo_lists_info.append(info)
                files_list.append(info['file_name'])

        with open('data.json', "w") as write_file:
            json.dump(photo_lists_info, write_file)

class YaUploader:
    def __init__(self, token: str):
        self.token = token_ya
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload(self):
        for file in tqdm(files_list):
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            params = {"path": put_to_dyrectory + '/' + file, "url": files_list_url[file]}
            response = requests.post(upload_url, params=params, headers=self.headers)
            if response.status_code != 202:
                print(f'\nОшибка {response.status_code}')
                quit()


    def create_folder(self, path_to_directory):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        requests.put(f'{url}?path={path_to_directory}', headers=self.headers)

if __name__ == '__main__':

    put_to_dyrectory = input(f"\nВведите название папки на Яндекс-диске: ")
    vk_client = VkUser(token_vk, version)
    vk_client.get_photo()
    token_ya = input(f"\nВведите токен Яндекс-диска: ")
    uploader = YaUploader(token_ya)
    print()
    uploader.create_folder(put_to_dyrectory)
    result = uploader.upload()
    print(f'\nКопирование файлов в папку: {put_to_dyrectory} , на Яндекс-Диск завершено.')
