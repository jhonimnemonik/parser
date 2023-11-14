import re
import time
import random
import requests
from parsers.base_parser import BaseParser


class KolesaParser(BaseParser):
    def start_parsing(self):
        try:
            result = self._get_html(self.url)
            soup = result[0]
            status = result[1]
            selector = int(soup.select_one('p.result-block__finded').text.split()[1])
            el = 1
            page_number = 1
            print('Статус подключения: ', status)
            print(f'Найдено {selector} объявлений')

            while True:
                random_sleep_time = random.randint(1, 3)
                link = f'{self.url}&page={page_number}'
                items = self.extract_items(link)
                if items is not None:
                    for item in items:
                        title = item.select_one('div.a-card__info > div.a-card__header > h5 > a').text.strip()
                        price = re.sub(r'\s+', '.', item.find(class_='a-card__price').text.strip())
                        description = item.find('p', class_='a-card__description').text.strip()
                        year = description.split()[0]
                        city = item.find('span', class_='a-card__param').text.strip()
                        record = {
                            'el': el,
                            'title': title,
                            'year': f'{year}го года выпуска',
                            'city': f'г.{city}',
                            'price': f'Цена: {price}',
                            'description': f'Описание: {description}'
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
        except requests.exceptions.RequestException as e:
            print(f'Не удалось получить доступ к странице: {url}, ошибка: {e}')
            return None

    def extract_items(self, link):
        result = self._get_html(link)
        if result:
            soup = result[0]
            items = soup.find_all('div', class_='a-card')
            return items
        else:
            return []


if __name__ == '__main__':
    # url = input('Введите ссылку с сайта kolesa.kz: ')
    url = 'https://kolesa.kz/cars/toyota/avtomobili-s-probegom/corolla/?generations[]=2036&price[to]=8500000'
    parser = KolesaParser(url)
    parser.start_parsing()
    parser.display_info(parser.data)
    parser.save_file()
