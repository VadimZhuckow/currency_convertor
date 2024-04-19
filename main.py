"""
Программа конвертации валют
Программа запрашивает у юзера валюту, сумму и валюту в которую нужно конвертировать
"""
import os
import requests
import json

DIR = os.getcwd()
FILE_NAME = 'key_access.txt'


def get_key_fo_service(file_name: str) -> str:
    """
    Функция для чтения файла в котором лежит ключ для сервиса
    :param file_name:
    :return:
    """
    with open(FILE_NAME) as file:
        key_serv = file.read().replace('\n', '')
    return key_serv


def get_file(current_dir, file_name):
    """
    Программа для проверки наличия файла в котором лежит ключ
    Если файла нет то программа создаст новый
    Так же если нет ключа то программа запросит ключ у юзера и запишет в файл
    :param current_dir:
    :param file_name:
    :return:
    """
    file_path = f"{current_dir}/{file_name}"
    if not os.path.exists(file_path):
        print(f"Файл {file_name} не существует, он будет создан")
        with open(FILE_NAME, 'w') as file:
            pass
            print('Файл создан')
    if os.stat(FILE_NAME).st_size == 0:
        user_key = input('Нет записанного ключа, введите ключ для сервиса по валютам: ')
        with open(FILE_NAME, 'w') as file:
            file.write(user_key)
            print('Ключ записан в файл')
        return get_key_fo_service(file_name)


def get_info_currency(file_name: str, key_api: str, currency: str) -> dict:
    """
    Из ответа от сервиса формируется словарь с валютой и значением валюты
    :param file_name:
    :param key_api:
    :param currency:
    :return:
    """
    key = get_key_fo_service(file_name)

    url = f"https://v6.exchangerate-api.com/v6/{key_api}/latest/{currency}"
    response = requests.get(url)
    data = response.json()
    currency_dict = {}
    for key, value in data['conversion_rates'].items():
        currency_dict[key] = value
    with open('currency.json', 'w') as file:
        file.write(json.dumps(currency_dict))

    return currency_dict


def get_available_currency(currency):
    with open('currency.json') as file:
        dict_currency = json.load(file)
        available_currency = [i for i in dict_currency.keys()]
        if currency not in available_currency:
            print("Такой валюты нет в списке, выберите валюту из списка: ")
            print(available_currency)
            return False
        else:
            return True


def convert(sum_, from_currency, to_currency, info_currency):
    for key, value in info_currency.items():
        if key == to_currency:
            print(f'За {sum_} {from_currency} получите {float(sum_) * value:.2f} {key}')


if __name__ == "__main__":
    print("Добро пожаловать в программу конвертации валют!")
    get_file(DIR, FILE_NAME)
    api_key = get_key_fo_service(FILE_NAME)
    # get_file(DIR, FILE_NAME)

    base_currency = input("Введите код исходной валюты (например, USD): ").upper()
    # get_info_currency(FILE_NAME, api_key, base_currency)
    flag = get_available_currency(base_currency)
    while not flag:
        base_currency = input('Введите валюту из списка: ').upper()
        flag = get_available_currency(base_currency)
    info_currency_list = get_info_currency(FILE_NAME, api_key, base_currency)
    summ = input('Введите сумму для конвертации, сумма должна быть числом: ')
    while not summ.isdigit():
        summ = input('Введите числовое значение: ')
    current_curency_sum = input('Введите код целевой валюты (например, RUB): ').upper()
    flag_surrent = get_available_currency(current_curency_sum)
    while not flag_surrent:
        current_curency_sum = input('Введите валюту из списка: ').upper()
        flag_surrent = get_available_currency(current_curency_sum)
    convert(summ, base_currency, current_curency_sum, info_currency_list)
