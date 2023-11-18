from parsers.medigence_com import MedigenceParser
from parsers.kolesa_kz import KolesaParser
from parsers.olx_pl import OlxParser


def main():
    print('Запуск парсера сайта kolesa.kz')
    url_1 = 'https://kolesa.kz/cars/toyota/avtomobili-s-probegom/corolla/?generations[]=2036&price[to]=8500000'
    kolesa_parser = KolesaParser(url_1)
    kolesa_parser.start_parsing()
    kolesa_parser.display_info(kolesa_parser.data)
    kolesa_parser.save_file()
    print('\nЗапуск парсера сайта medigence.com')
    url_2 = 'https://medigence.com/ru/hospitals/all/all/turkey'
    medigence_parser = MedigenceParser(url_2)
    medigence_parser.start_parsing()
    medigence_parser.display_info(medigence_parser.data)
    medigence_parser.save_file()
    print('\nЗапуск парсера сайта olx.pl')
    url_3 = ('https://www.olx.pl/krakow/q-laptop/?search%5Bfilter_float_price:to%5D=1000&search'
           '%5Bfilter_enum_operatingsystem_laptops%5D%5B0%5D=windows10&search%5Bfilter_enum_operatingsystem_laptops'
           '%5D%5B1%5D=windows11&search%5Bfilter_enum_processorseries_laptops%5D%5B0%5D=intel-core-i9&search'
           '%5Bfilter_enum_processorseries_laptops%5D%5B1%5D=apple-m&search%5Bfilter_enum_processorseries_laptops%5D'
           '%5B2%5D=intel-core-i7&search%5Bfilter_enum_processorseries_laptops%5D%5B3%5D=intel-core-i5&search'
           '%5Bfilter_enum_processorseries_laptops%5D%5B4%5D=intel-core-i3&search%5Bfilter_enum_ramsize_laptops%5D'
           '%5B0%5D=6gb-12gb&search%5Bfilter_enum_screendiagonal_laptops%5D%5B0%5D=15-15-9&search'
           '%5Bfilter_enum_screendiagonal_laptops%5D%5B1%5D=16-and-more&search%5Bfilter_enum_state%5D%5B0%5D=used'
           '&search%5Bfilter_enum_state%5D%5B1%5D=new')
    olx_parser = OlxParser(url_3)
    olx_parser.start_parsing()
    olx_parser.display_info(olx_parser.data)
    olx_parser.save_file()
    print('\nРабота парсеров завершенна')


if __name__ == '__main__':
    main()
