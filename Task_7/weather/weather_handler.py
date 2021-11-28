import json
from datetime import datetime
from typing import Any, Tuple, List, Dict
from typing import Union

import datefinder
import spacy

from weather.weather import make_forecast


class WeatherNEExtractor:
    __short_name_path = "data/short_names.json"

    def __init__(self):
        self.__short_names = self.__load_short_names()

    def __load_short_names(self) -> Dict[str, str]:
        with open(self.__short_name_path) as file:
            short_names = json.load(file)

        return short_names

    def extract_ne(self, message: str):
        return self.__get_ne(message)

    def __get_city(self, message: str) -> str:
        nlp = spacy.load("ru_core_news_sm")
        doc = nlp(message)

        city = None

        for i, ent in enumerate(doc.ents):
            if ent.label_ == 'LOC':
                city = ent.lemma_.title()

        for w in message.split():
            for k in self.__short_names:
                if k in w:
                    return self.__short_names[k]
        return city

    @staticmethod
    def __get_dates_by_datefinder(message: str) -> List[datetime]:
        return [match for match in datefinder.find_dates(message)]

    def __get_dates(self, message: str) -> Tuple[int, int, Any]:
        # прогноз на сегодня
        # прогноз на завтра
        # прогноз на послезавтра
        # прогноз на неделю вперед, начиная с текущей даты

        message = message.lower()

        day_start, day_end = None, None

        if 'сегодня' in message or 'сейчас' in message:
            day_start, day_end = 0, 0
        if 'завтра' in message:
            day_start, day_end = 1, 0
        if 'послезавтра' in message:
            day_start, day_end = 2, 0
        if 'на неделю' in message:
            day_start, day_end = 0, 7

        if day_start is None:
            day_start, day_end = 0, 0

        dates = self.__get_dates_by_datefinder(message)

        return day_start, day_end, dates

    def __get_ne(self, message: str):
        # требуем писать города с большой буквы
        city = self.__get_city(message)
        date_start, date_end, dates = self.__get_dates(message)
        return city, date_start, date_end, dates


class WeatherFeature:
    __ending_responses = [
        "Тебе ещё что-то подсказать?",
        "Не хочешь узнать новости или посмотреть цены на билеты?"
    ]

    def __init__(self):
        self.__extractor = WeatherNEExtractor()

    def handle(self, text: str) -> Union[str, List[str]]:
        city, date_start, date_end, dates = self.__extractor.extract_ne(text)

        if city is None:
            message = f"Прости, не смог найти такой город"
            return message

        if len(dates) == 1:
            if dates[0].date() < datetime.today().date():
                message = 'Дата меньше текущей :('
                return message

        if len(dates) == 2:
            print(dates[0].date(), datetime.today().date())
            if dates[0].date() < datetime.today().date() or dates[1].date() < datetime.today().date():
                message = 'Неверный диапазон дат :('
                return message

        forecast = make_forecast(city, date_start, date_end, dates)

        if isinstance(forecast, str):
            forecast = [forecast]

        return forecast
