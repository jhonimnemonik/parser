import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
from parsers import base_parser


class MedigenceParser(base_parser.BaseParser):
    def _get_html(self, url):
        try:
            driver = webdriver.Chrome()
            status = requests.get(url).status_code
            driver.get(url)
            wdw(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
            while True:
                target_element = wdw(driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH,
                         "//button[@class='bg-red-1 btn fs-18 px-5 py-2 rounded-3 text-white' and @id='paginator']")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
                time.sleep(2)
                target_element.click()
                wdw(driver, 10).until(ec.invisibility_of_element_located((By.ID, "loading-spinner")))
                time.sleep(2)
                if "No More Data" in target_element.text:
                    break
                next_element = wdw(driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//button[@class='bg-red-1 btn fs-18 px-5 py-2 rounded-3 "
                                   "text-white' and @id='paginator']")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_element)
                time.sleep(2)
            wdw(driver, 10).until(ec.invisibility_of_element_located((By.ID, "loading-spinner")))
            data_html = driver.page_source
        finally:
            driver.quit()
        class_name = self.__class__.__name__
        if status == 200:
            with open(f'../htmls/{class_name}.html', 'w', encoding='utf-8') as file:
                file.write(data_html)
            with open(f'../htmls/{class_name}.html', 'r', encoding='utf-8') as file:
                html = file.read()
            soup = bs(html, 'html.parser')
            items = soup.find_all(class_='border hospital-card mb-3 p-3 rounded-4 shadow')
            return items, soup, status
        else:
            print(f'Не удалось получить доступ к странице: {url}, ошибка {status}')
            return None

    def start_parsing(self):
        try:
            result = self._get_html(self.url)
            items = result[0]
            soup = result[1]
            status = result[2]
            selector = int(soup.select_one('#hospital-results span.me-1').text)
            el = 1
            print('Статус подключения: ', status)
            print(f'Найдено {selector} объявлений')
            while True:
                if items:
                    for item in items:
                        title = item.find('span', itemprop='name').text
                        city = item.find('p', class_='gt-block fs-18 mb-0').text.strip()
                        descript = item.find(class_='hospital_content overflow-hidden text-gray-1').text.strip()
                        item_url = item.find('a', class_='text-decoration-none text-red-1')['href']
                        assessments = item.find('div', class_='align-items-center pt-4 row').text
                        record = {
                            'el': el,
                            'title': title,
                            'city': f'Город: {city}',
                            'descript': f'Описание:{descript}',
                            'url': f'Cсылка: {item_url}',
                            'assessments': f'Оценки: {assessments}'
                        }
                        print(el, title, city)
                        self.data.append(record)
                        el += 1
                else:
                    break
                if el > selector:
                    break
            return self.data
        except requests.exceptions.RequestException as e:
            print(f'Не удалось получить доступ к странице: {self.url}, ошибка: {e}')
            return None

if __name__ == '__main__':
    url = 'https://medigence.com/ru/hospitals/all/all/turkey'
    parser = MedigenceParser(url)
    parser.start_parsing()
    parser.display_info(parser.data)
    parser.save_file()
