import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from collections import OrderedDict

class OlxParser:
    def __init__(self, url):
        self.url = url
        self.data = []

    def get_html(self, url):
        # headers = {"User-Agent": user_agent}
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            items = soup.find_all('div', class_="listing-grid-container css-d4ctjd")
            # items = soup.findAll(class_='css-oukcj3')
            return items, soup, status
        else:
            print(f'Не удалось получить доступ к странице: {url}, ошибка {response.status_code}')
            return None

    def start_parsing(self):
        try:
            result = self.get_html(self.url)
            soup = result[1]
            status = result[2]
            selector = int(soup.select_one("div.css-n9feq4 > span > span").text.split()[1])
            el = 1
            print('Статус подключения: ', status)
            print(f'Найдено {selector} объявлений')
            part1, part2 = self.url.split('?', 1)
            page_num = 1

            while el <= selector:
                random_sleep_time = random.randint(1, 3)
                page = f'?page={page_num}&'
                link = f'{part1}{page}{part2}'
                items = self.get_html(link)[0]
                if items:
                    for item in items:
                    # for item in  soup.find('div', attrs={'data-testid': 'listing-grid', 'class': 'css-oukcj3'}):
                    # for item in  soup.find_all('div', {'class': 'css-oukcj3'}):
                        title = item.select_one('div.css-u2ayx9 > h6').text.strip()
                        price = item.find(class_='css-10b0gli er34gjf0').text.split()[0]
                        descript = item.find(class_='css-odp1qd').text.split('-')
                        city = descript[0].strip()
                        date = descript[1].strip()
                        item_url = 'https://www.olx.pl' + item.find('a', class_='css-rc5s2u').get('href')
                        image = item.find('a', class_='css-rc5s2u').find('img')['src']
                        record = {
                            'el': el,
                            'title': title,
                            'price': f'Цена: {price}',
                            'date': f'Дата публикации: {date}',
                            'city': f'Город: {city}',
                            'url': f'Cсылка: {item_url}',
                            'image': f'Картинка: {image}'
                        }
                        print(el, title, city, price)
                        self.data.append(record)
                        el += 1
                        time.sleep(0.25)
                    time.sleep(random_sleep_time)
                else:
                    break
                if el > selector:
                    break
                page_num += 1
            return self.data
        except requests.exceptions.RequestException as e:
            print(f'Не удалось получить доступ к странице: {self.url}, ошибка: {e}')
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
            file_name = 'otodomPL'
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
    # url = input('Введите ссылку с сайта olx.pl: ')
    url = 'https://www.olx.pl/krakow/q-laptop/?search%5Bfilter_enum_operatingsystem_laptops%5D%5B0%5D=windows10&search%5Bfilter_enum_operatingsystem_laptops%5D%5B1%5D=windows11&search%5Bfilter_enum_processorseries_laptops%5D%5B0%5D=intel-core-i9&search%5Bfilter_enum_processorseries_laptops%5D%5B1%5D=apple-m&search%5Bfilter_enum_processorseries_laptops%5D%5B2%5D=intel-core-i7&search%5Bfilter_enum_processorseries_laptops%5D%5B3%5D=intel-core-i5&search%5Bfilter_enum_processorseries_laptops%5D%5B4%5D=intel-core-i3&search%5Bfilter_enum_ramsize_laptops%5D%5B0%5D=6gb-12gb&search%5Bfilter_enum_screendiagonal_laptops%5D%5B0%5D=15-15-9&search%5Bfilter_enum_screendiagonal_laptops%5D%5B1%5D=16-and-more&search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bfilter_enum_state%5D%5B1%5D=new'
    parser = OlxParser(url)
    parser.get_html(url)
    parser.start_parsing()
    # parser.display_info(parser.data)
    # parser.save_file()
