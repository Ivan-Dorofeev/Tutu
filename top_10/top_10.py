import collections
import re

import requests as requests
from bs4 import BeautifulSoup

url_name = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
url_flights = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'


def parser():
    airports_dict = {}
    top_10_list = []
    """Спарсим номера и названия аэропортов в словарь airports_dict """
    response1 = requests.get(url_name)
    if response1.status_code == 200:
        html_page = BeautifulSoup(response1.text, 'html.parser')
        airports = str(html_page).split('\n')
        for i in airports:
            if len(i) > 2:
                airports_dict[i.split(',')[4][1:-1]] = i.split(',')[1]
            else:
                break
        # print(airports_dict)
    else:
        print(f'Oops, ошибка запроса на сайт - {response1.status_code}')

    """Спарсим номера и названия аэропортов в словарь flieghts_dict """
    response2 = requests.get(url_flights)
    if response2.status_code == 200:
        html_page = BeautifulSoup(response2.text, 'html.parser')
        flights = str(html_page).split('\n')
        flights_ab = []
        for i in flights:
            if len(i) > 4:
                flights_ab.append(i.split(',')[2] + i.split(',')[4])
            else:
                break
        top_10_list = collections.Counter(flights_ab).most_common(10)
        # print(top_10_list)
    else:
        print(f'Oops, ошибка запроса на сайт - {response2.status_code}')

    result = []
    for i in top_10_list:
        air_name_out = i[0][:3]
        air_name_in = i[0][3:]
        if air_name_in in airports_dict.keys():
            if air_name_out in airports_dict.keys():
                result.append([airports_dict[air_name_in],airports_dict[air_name_out],i[1]])

    for i in result:
        print(f' Аэропорта вылета {i[0]}, Аэропорт прилёта {i[1]}, {i[2]} раз встречалось направление')


if __name__ == '__main__':
    parser()
