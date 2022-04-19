import os
import requests
from datetime import datetime
import json
import shutil
from tqdm import tqdm

token_vk = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
version = '5.131'
files_list = []

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
        photo_lists_info = []
        os.mkdir(put_to_dyrectory)
        for photo in photo_lists['response']['items']:
            info = {'file_name': str(photo['likes']['count']) +'.jpg',
                    'size': photo['sizes'][-1]['type']}
            info_1 = {'file_name': str(photo['likes']['count']) + '_' + str(datetime.fromtimestamp(photo['date']).date()) + '.jpg',
                    'size': photo['sizes'][-1]['type']}
            if info['file_name'] in files_list:
                image_bin = requests.get(photo['sizes'][-1]['url'])
                open(f"{put_to_dyrectory}/{info_1['file_name']}", 'wb').write(image_bin.content)
                photo_lists_info.append(info_1)
                files_list.append(info_1['file_name'])
            else:
                image_bin = requests.get(photo['sizes'][-1]['url'])
                open(f'{put_to_dyrectory}/{info["file_name"]}', 'wb').write(image_bin.content)
                photo_lists_info.append(info)
                files_list.append(info['file_name'])

        with open(f'{put_to_dyrectory}/data.json', "w") as write_file:
            json.dump(photo_lists_info, write_file)
            files_list.append('data.json')

class YaUploader:
    def __init__(self, token: str):
        self.token = token_ya

    def upload(self):
        for file in tqdm(files_list):
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
            }
            params = {"path": put_to_dyrectory + '/' + file, "overwrite": "true"}
            response = requests.get(upload_url, headers=headers, params=params)
            href = response.json()['href']
            response = requests.put(href, data=open(put_to_dyrectory + '/' + file, 'rb'))
            response.raise_for_status()

    def create_folder(self, path_to_directory):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        requests.put(f'{url}?path={path_to_directory}', headers=headers)


if __name__ == '__main__':

    put_to_dyrectory = input(f"\nВведите название папки на Яндекс-диске: ")
    vk_client = VkUser(token_vk, version)
    vk_client.get_photo()
    token_ya = input(f"\nВведите токен Яндекс-диска: ")
    uploader = YaUploader(token_ya)
    print()
    uploader.create_folder(put_to_dyrectory)
    result = uploader.upload()
    shutil.rmtree(put_to_dyrectory, ignore_errors=False)
    print(f'\nКопирование файлов в папку: {put_to_dyrectory} , на Яндекс-Диск завершено.')
