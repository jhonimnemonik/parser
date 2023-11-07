import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json
import os
from collections import OrderedDict


class KolesaParser:
    def __init__(self, url):
        self.url = url
        self.data = []

    def _get_html(self, url):
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            car = soup.find_all('div', class_='a-card')
            return car, soup, status
        else:
            print(f'Не удалось получить доступ к странице: {url}, ошибка {response.status_code}')
            return None

    def start_parsing(self):
        try:
            result = self._get_html(url)
            soup = result[1]
            status = result[2]
            selector = int(soup.select_one('p.result-block__finded').text.split()[1])
            el = 1
            page_number = 1
            print('Статус подключения: ', status)
            print(f'Найдено {selector} объявлений')

            while True:
                random_sleep_time = random.randint(1, 3)
                link = f'{self.url}&page={page_number}'
                car = self._get_html(link)[0]
                if car is not None:
                    for info in car:
                        title = info.select_one('div.a-card__info > div.a-card__header > h5 > a').text.strip()
                        price = re.sub(r'\s+', '.', info.find(class_='a-card__price').text.strip())
                        description = info.find('p', class_='a-card__description').text.strip()
                        year = description.split()[0]
                        city = info.find('span', class_='a-card__param').text.strip()
                        record = {
                            'el': el,
                            'title': title,
                            'year': f'{year}го года выпуска',
                            'city': f'г.{city}',
                            'price': f'Цена: {price}',
                            'description': f'Описание: {description}'
                        }
                        print(el, city, price)
                        self.data.append(record)
                        el += 1
                    time.sleep(random_sleep_time)
                else:
                    break
                if el > selector:
                    break
                page_number += 1
            return self.data
        except requests.exceptions.RequestException as e:
            print(f'Не удалось получить доступ к странице: {url}, ошибка: {e}')
            return None

    def display_info(self, data):
        for item in data:
            el = item['el']
            title = item['title']
            year = item['year']
            price = item['price']
            city = item['city']
            description = item['description']
            info_str = f'{el} - {title}: Год выпуска: {year}, Цена: {price}, Город: {city}\nОписание: {description}\n'
            print(info_str)

    def save_file(self):
        try:
            file_name = 'kolesaKZ'
            output_dir = 'Data'
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
    url = input(
        'Введите ссылку с сайта kolesa.kz: ')  # 'https://kolesa.kz/cars/toyota/avtomobili-s-probegom/corolla/?generations[]=2036'
    parser = KolesaParser(url)
    parser.start_parsing()
    parser.display_info(parser.data)
    parser.save_file()
