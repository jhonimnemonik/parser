import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json

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
            print(f"Не удалось получить доступ к странице: {url}, ошибка {response.status_code}")
            return None

    def display_info(self, data):
        for item in data:
            el = item['el']
            title = item['title']
            year = item['year']
            price = item['price']
            city = item['city']
            description = item['description']
            info_str = f"{el} - {title}: Год выпуска: {year}, Цена: {price}, Город: {city}\nОписание: {description}\n"
            print(info_str)

    def start_parsing(self):
        status = self._get_html(url)[2]
        first_iteration = True
        el = 1
        page_number = 1
        random_sleep_time = random.randint(1, 3)
        print('Статус подключения: ', status)

        while True:
            link = f'{self.url}&page={page_number}'
            response, soup, _ = self._get_html(link)
            car = response
            selector = int(soup.select_one('p.result-block__finded').text.split()[1])

            if car is not None:
                if first_iteration:
                    for info in car:
                        title = info.select_one('div.a-card__info > div.a-card__header > h5 > a').text.strip()
                        price = re.sub(r'\s+', '.', info.find(class_='a-card__price').text.strip())
                        description = info.find('p', class_='a-card__description').text.strip()
                        year = description.split()[0]
                        city = info.find('span', class_="a-card__param").text.strip()
                        record = {
                            "el": el,
                            "title": title,
                            "year": f"{year}го года выпуска",
                            "city": f"г.{city}",
                            "price": f"Цена: {price}",
                            "description": f"Описание: {description}"
                        }
                        el += 1
                        self.data.append(record)
                    first_iteration = False
                    time.sleep(3)
                else:
                    for info in car:
                        title = info.select_one('div.a-card__info > div.a-card__header > h5 > a').text.strip()
                        price = re.sub(r'\s+', '.', info.find(class_='a-card__price').text.strip())
                        description = info.find('p', class_='a-card__description').text.strip()
                        year = description.split()[0]
                        city = info.find('span', class_="a-card__param").text.strip()
                        record = {
                            "el": el,
                            "title": title,
                            "year": f"{year}го года выпуска",
                            "city": f"г.{city}",
                            "price": f"Цена: {price}",
                            "description": f"Описание: {description}"
                        }
                        self.data.append(record)
                        el += 1
                    time.sleep(random_sleep_time)
            else:
                break
            if el > selector:
                break
            page_number += 1
        return self.data

    def save_to_json(self):
        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4)
        print(f"Данные успешно записаны в файл 'output.json'\nВсего добавлено {len(self.data)} позиций")


if __name__ == '__main__':
    url = 'https://kolesa.kz/cars/toyota/avtomobili-s-probegom/corolla/?generations[]=2036'
    parser = KolesaParser(url)
    parser.start_parsing()
    parser.save_to_json()
    parser.display_info(parser.data)
