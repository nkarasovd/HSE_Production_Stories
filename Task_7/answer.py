import os.path
import random
import re
from typing import List, Optional

import spacy

from weather.weather_handler import WeatherFeature

_greeting = ["Привет!", "Здравствуй!", "Привет, начнем."]
_bye = ["Пока!", "До свидания!", "Рад был пообщаться!"]


class IntentRecognizer:
    _data_path = "./data"

    def __init__(self, intents: Optional[List[str]] = None):
        self._nlp = spacy.load("ru_core_news_sm")
        self._intents = {}

        if intents is not None:
            for intent in intents:
                file_path = os.path.join(self._data_path, intent + ".txt")

                with open(file_path, 'r') as f:
                    examples = f.readlines()
                    self._intents[intent] = self._preprocessing(examples)

    @staticmethod
    def _preprocessing(examples: List[str]):
        result = []

        for example in examples:
            example = example.strip()
            example = example.lower()
            result.append(re.sub(r'[^\w\s]', '', example))

        return result

    def get_intents(self, text):
        if len(self._intents) == 0:
            return []

        tokens = [str(token.lemma_) for token in self._nlp(text)]

        intents = []
        for intent, examples in self._intents.items():
            examples = [str(token.lemma_) for token in self._nlp(' '.join(examples))]

            if set(tokens).intersection(set(examples)):
                intents.append(intent)

        return intents


class MessageHandler:
    _default_phrases = [
        "Извини, я тебя не понял.",
        "Можешь уточнить, пожалуйста?",
        "Что, что?",
        "Я про такое не слышал.",
        "Я не понял, скажи иначе, пожалуйста."
    ]

    def __init__(self):
        self._intent_recognizer = IntentRecognizer(["greeting", "bye", "weather"])
        self._weather_handler = WeatherFeature()

    def get_answer(self, text: str):
        intents = self._intent_recognizer.get_intents(text)

        if len(intents) == 0:
            return random.choice(self._default_phrases)

        if len(intents) == 1:
            if intents[0] == "greeting":
                return random.choice(_greeting)
            if intents[0] == "bye":
                return random.choice(_bye)
            if intents[0] == "weather":
                return self._weather_handler.handle(text)
        else:
            return random.choice(self._default_phrases)
