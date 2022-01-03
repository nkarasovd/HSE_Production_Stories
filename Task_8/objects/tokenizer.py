import re
from typing import List

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


class Tokenizer:
    def __init__(self, n: int = 1):
        self.n = n

        self.stopwords = stopwords.words("english") + ["doesnt"]
        self.lemmatizer = WordNetLemmatizer()

    @staticmethod
    def preprocess(text: str) -> List[str]:
        text = text.replace('.', ' ')
        return text.lower().split()

    def tokenize(self, text: str) -> List[str]:
        regex = re.compile('[^a-zA-Z]')
        tokens = [regex.sub('', token) for token in self.preprocess(text)]
        tokens = [token for token in tokens if token not in self.stopwords]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if len(token) > 0]

        return [" ".join(tokens[i - self.n + 1: i + 1]) for i in range(self.n - 1, len(tokens))]

    def __call__(self, text: str) -> List[str]:
        return self.tokenize(text)
