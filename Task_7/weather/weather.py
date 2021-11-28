import datetime
import json
import os
from typing import Dict, List, Callable, Any

import requests

with open("environment.env", 'r') as f:
    vars_dict = dict(
        tuple(line.split('='))
        for line in f.readlines() if not line.startswith('#')
    )

os.environ.update(vars_dict)

API_KEY = os.getenv("WEATHER_API_KEY").strip()
URL_DAILY = f'https://api.weatherbit.io/v2.0/forecast/daily?key={API_KEY}'
URL_CURRENT = f'https://api.weatherbit.io/v2.0/current?key={API_KEY}'


def _weather_in_city(city_name: str, days: int, skip_days: List = None) -> str:
    querystring = {'city': city_name, 'days': days, 'lang': 'ru'}
    return _weather_by_days(city_name=city_name, params=querystring, skip_days=skip_days)


def _weather_in_city_by_coords(lat, lon, days: int) -> str:
    querystring = {'lat': lat, 'lon': lon, 'days': days, 'lang': 'ru'}
    return _weather_by_days(params=querystring)


def _current_weather_in_city(city_name: str) -> str:
    querystring = {'city': city_name, 'lang': 'ru'}
    return _current_weather(city_name=city_name, params=querystring)


def _current_weather_by_coords(lat, lon) -> str:
    querystring = {'lat': lat, 'lon': lon, 'lang': 'ru'}
    return _current_weather(params=querystring)


def _add_forecast(forecast: str, data_dict: Dict[str, Any], condition: Callable[[int, str], bool]) -> str:
    for i, day in enumerate(data_dict['data']):
        date = day['valid_date']
        if condition(i, date):
            description = day['weather']['description'].lower()
            temp_min = day['min_temp']
            temp_max = day['max_temp']
            wind_spd = round(day['wind_spd'], 1)
            wind_dir = day['wind_cdir_full'].lower()

            message = f'\t– {date}: {description}, температура воздуха от {temp_min}\N{DEGREE SIGN}C до' \
                      f' {temp_max}\N{DEGREE SIGN}C,' \
                      f' скорость ветра – {wind_spd} м/с, ветер {wind_dir}.'

            forecast += '\n' + message

    return forecast


def _weather_by_days(city_name: str = None, params: Dict = None, skip_days: List = None) -> str:
    response = requests.request("GET", URL_DAILY, params=params)
    data_dict = json.loads(response.text)

    if city_name is None:
        city_name = data_dict['city_name']

    forecast = f'Прогноз погоды в городе {city_name}.'

    if skip_days is not None:
        start, end = skip_days
        condition = lambda i, date: start <= i < end
    else:
        condition = lambda i, date: True

    return _add_forecast(forecast, data_dict, condition)


def _current_weather(city_name: str = None, params: Dict = None) -> str:
    response = requests.request("GET", URL_CURRENT, params=params)

    data_dict = json.loads(response.text)

    temp = data_dict['data'][0]['temp']
    wind_spd = round(data_dict['data'][0]['wind_spd'], 1)
    description = data_dict['data'][0]['weather']['description'].lower()
    wind_dir = data_dict['data'][0]['wind_cdir_full'].lower()

    if city_name is None:
        city_name = data_dict['data'][0]['city_name']

    message = f'Погода в городе {city_name}: {description}, температура воздуха – {temp}\N{DEGREE SIGN}C,' \
              f' скорость ветра – {wind_spd} м/с, ветер {wind_dir}.'

    return message


def _weather_by_dates(city_name: str = None, dates=None) -> str:
    params = {'city': city_name, 'days': 20, 'lang': 'ru'}
    response = requests.request("GET", URL_DAILY, params=params)

    if len(dates) == 1:
        start_date = dates[0].date().__str__()
        end_date = dates[0] + datetime.timedelta(days=1)
        end_date = end_date.date().__str__()
    elif len(dates) == 2:
        start_date = dates[0].date().__str__()
        end_date = dates[1] + datetime.timedelta(days=1)
        end_date = end_date.date().__str__()

    data_dict = json.loads(response.text)

    if city_name is None:
        city_name = data_dict['city_name']

    forecast = f'Прогноз погоды в городе {city_name}.'

    condition = lambda i, date: start_date <= date < end_date

    return _add_forecast(forecast, data_dict, condition)


def make_forecast(city: str, date_start: int, date_end: int, dates: List):
    # указаны конкретные даты
    if dates:
        return _weather_by_dates(city, dates)
    # прогноз на текущий день
    if date_start == 0 and date_end == 0:
        return _current_weather_in_city(city)
    # прогноз на неделю вперед
    if date_start == 0 and date_end == 7:
        return _weather_in_city(city, 7)
    # прогноз на завтра
    if date_start == 1 and date_end == 0:
        return _weather_in_city(city, 2, skip_days=[1, 2])
    # прогноз на послезавтра
    if date_start == 2 and date_end == 0:
        return _weather_in_city(city, 3, skip_days=[2, 3])
