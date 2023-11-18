import time
import random
from parsers.base_parser import BaseParser
import requests


class OlxParser(BaseParser):
    def start_parsing(self):
        try:
            result = self._get_html(self.url)
            soup = result[0]
            status = result[1]
            selector = int(soup.select_one("div.css-n9feq4 > span > span").text.split()[1])
            el = 1
            print('Статус подключения: ', status)
            print(f'Найдено {selector} объявлений')
            part1, part2 = self.url.split('?', 1)
            page_num = 1
            while True:
                random_sleep_time = random.randint(1, 3)
                page = f'?page={page_num}&'
                link = f'{part1}{page}{part2}'
                new_soup = (self._get_html(link))[0]
                items = new_soup.select(".css-oukcj3 > .css-1sw7q4x")
                if items:
                    for item in items:
                        title = item.find(class_="css-16v5mdi er34gjf0").text.strip()
                        price = item.find(class_='css-10b0gli er34gjf0').text.split('zl')[0]
                        descript = item.find(class_='css-odp1qd').text.split(' - ')
                        city = descript[0].strip()
                        date = descript[1].strip()
                        item_url = 'https://www.olx.pl' + item.find('a', class_='css-rc5s2u').get('href')
                        image = item.find('img')['src']
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
                        if el >= selector:
                            break
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

if __name__ == '__main__':
    # url = input('Введите ссылку с сайта olx.pl: ')
    url = ('https://www.olx.pl/krakow/q-laptop/?search%5Bfilter_float_price:to%5D=1000&search'
           '%5Bfilter_enum_operatingsystem_laptops%5D%5B0%5D=windows10&search%5Bfilter_enum_operatingsystem_laptops'
           '%5D%5B1%5D=windows11&search%5Bfilter_enum_processorseries_laptops%5D%5B0%5D=intel-core-i9&search'
           '%5Bfilter_enum_processorseries_laptops%5D%5B1%5D=apple-m&search%5Bfilter_enum_processorseries_laptops%5D'
           '%5B2%5D=intel-core-i7&search%5Bfilter_enum_processorseries_laptops%5D%5B3%5D=intel-core-i5&search'
           '%5Bfilter_enum_processorseries_laptops%5D%5B4%5D=intel-core-i3&search%5Bfilter_enum_ramsize_laptops%5D'
           '%5B0%5D=6gb-12gb&search%5Bfilter_enum_screendiagonal_laptops%5D%5B0%5D=15-15-9&search'
           '%5Bfilter_enum_screendiagonal_laptops%5D%5B1%5D=16-and-more&search%5Bfilter_enum_state%5D%5B0%5D=used'
           '&search%5Bfilter_enum_state%5D%5B1%5D=new')
    parser = OlxParser(url)
    parser.start_parsing()
    parser.display_info(parser.data)
    parser.save_file()
