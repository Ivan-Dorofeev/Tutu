from sys import getsizeof
import requests as requests


def parser_airports():
    """ Парсим короткие и полные названия аэропортов в словарь airports_dict """

    url1 = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
    airports_dict = {}
    for i in str(requests.get(url1).text).split('\n'):
        if len(i) > 2:
            airports_dict[i.split(',')[4][1:-1]] = i.split(',')[1]
        else:
            break
    return airports_dict


def parser_routes():
    """ Парсим короткие названия аэропортов, находим кол-во их повторений """

    url2 = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'
    flights_dict = {}
    size_file = len(requests.get(url2).text.split('\n'))
    for i in range(0, size_file + 1):
        file_string = requests.get(url2).text.split('\n')[i]
        flight = file_string.split(',')[2] + file_string.split(',')[4]
        if flight in flights_dict.keys():
            flights_dict[flight] += 1
        else:
            flights_dict[flight] = 1
    # Вычисляем топ 10 частых направлений из словаря flights_dict
    count = 0
    res = []
    for w in sorted(flights_dict, key=flights_dict.get, reverse=True):
        count += 1
        if count == 11:
            break
        res.append([w, flights_dict[w]])
    return res


def main():
    """ Формируем список на вывод, выводим """
    top_10_list = parser_routes()
    airports_dict = parser_airports()
    print(round(int(getsizeof(top_10_list)) / 1000000, 4), ' Mb')
    print(round(int(getsizeof(airports_dict)) / 1000000, 3), ' Mb')
    result = []
    counter = 0
    for i in top_10_list:
        airport_name_out = i[0][:3]
        airport_name_in = i[0][3:]
        if airport_name_in in airports_dict.keys():
            if airport_name_out in airports_dict.keys():
                result.append([airports_dict[airport_name_in], airports_dict[airport_name_out], i[1]])
    for i in result:
        counter += 1
        print(f'{counter}. [{i[0]}]  [{i[1]}]  [{i[2]}]')


if __name__ == '__main__':
    parser_routes()

# ключей в routes 37595, 1.31  Mb
