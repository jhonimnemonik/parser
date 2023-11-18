from abc import ABC, abstractmethod
import json
import os
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup


class BaseParser(ABC):
    def __init__(self, url):
        self.url = url
        self.data = []

    def _get_html(self, url):
        st_accept = 'text/html'
        st_useragent = (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/15.4 Safari/605.1.15'
        )
        headers = {
            'User-Agent': st_useragent,
            'Accept': st_accept
        }
        response = requests.get(url, headers=headers)
        status = response.status_code
        class_name = self.__class__.__name__
        if status == 200:
            htmls_directory = '../htmls'
            if not os.path.exists(htmls_directory):
                os.makedirs(htmls_directory)
            if status == 200:
                with open(f'{htmls_directory}/{class_name}.html', 'w', encoding='utf-8') as file:
                    file.write(response.text)
                with open(f'{htmls_directory}/{class_name}.html', 'r', encoding='utf-8') as file:
                    html = file.read()
            soup = BeautifulSoup(html, 'html.parser')
            return soup, status
        else:
            print(f'Не удалось получить доступ к странице: {url}, ошибка {response.status_code}')
            return None

    @abstractmethod
    def start_parsing(self):
        pass

    def display_info(self, data):
        for item in data:
            info_str = f'{item["el"]} - {item["title"]}: '
            for key, value in item.items():
                if key not in ["el", "title"]:
                    info_str += f'\n{value}, '
            info_str = info_str.rstrip(', ')
            print(info_str)
            print()

    def save_file(self):
        try:
            class_name = self.__class__.__name__
            file_name = class_name.split('Parser')[0]
            output_dir = 'data'
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            file_path = os.path.join(output_dir, file_name + '.json')
            existing_data = []
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as existing_file:
                    existing_data = json.load(existing_file, object_pairs_hook=OrderedDict)
            combined_data = existing_data + self.data
            num_new_positions = len(combined_data) - len(existing_data)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(combined_data, file, ensure_ascii=False, indent=4)
            print(f'Данные успешно записаны в файл {file_name}\nВсего добавлено {num_new_positions} новых позиций')
        except Exception as e:
            print(f'Произошла ошибка при сохранении файла: {str(e)}')


if __name__ == '__main__':
    BaseParser
