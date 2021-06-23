import collections
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
    top_10_flights = collections.Counter(
        [i.split(',')[2] + i.split(',')[4] for i in requests.get(url2).text.split('\n') if len(i) > 4]).most_common(10)
    return top_10_flights


def main():
    """ Формируем список на вывод, выводим """
    top_10_list = parser_routes()
    airports_dict = parser_airports()
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
    main()

# Вывод
#
# Размер top_10_list: 0.001432  Mb
# Размер airports_dict: 1.11528  Mb
# 1. ["Hartsfield Jackson Atlanta International Airport"]  ["Chicago O'Hare International Airport"]  [20]
# 2. ["Chicago O'Hare International Airport"]  ["Hartsfield Jackson Atlanta International Airport"]  [19]
# 3. ["Suvarnabhumi Airport"]  ["Phuket International Airport"]  [13]
# 4. ["Louis Armstrong New Orleans International Airport"]  ["Chicago O'Hare International Airport"]  [13]
# 5. ["Miami International Airport"]  ["Hartsfield Jackson Atlanta International Airport"]  [12]
# 6. ["Muscat International Airport"]  ["Abu Dhabi International Airport"]  [12]
# 7. ["Bahrain International Airport"]  ["Hamad International Airport"]  [12]
# 8. ["London Heathrow Airport"]  ["John F Kennedy International Airport"]  [12]
# 9. ["John F Kennedy International Airport"]  ["London Heathrow Airport"]  [12]
# 10. ["Hartsfield Jackson Atlanta International Airport"]  ["Miami International Airport"]  [12]
# --- 0.98 seconds ---
