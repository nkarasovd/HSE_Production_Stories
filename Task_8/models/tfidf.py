from typing import List

import numpy as np

from objects.dataloader import Dataloader
from objects.tokenizer import Tokenizer


class TfIdfModel:
    def __init__(self, tokenizer: Tokenizer, n: int = 7):
        self.tokenizer = tokenizer
        self.n = n

    @staticmethod
    def get_tf(tokens_corpus: List[List[str]]):
        tf_dict, total_words_num = {}, sum(map(len, tokens_corpus))

        for tokens in tokens_corpus:
            for token in tokens:
                tf_dict[token] = tf_dict.get(token, 0) + 1

        return {k: v / total_words_num for k, v in tf_dict.items()}

    @staticmethod
    def get_idf(tokens_corpus: List[List[str]]):
        idf_dict = {}

        for tokens in tokens_corpus:
            for token in set(tokens):
                idf_dict[token] = idf_dict.get(token, 0) + 1

        return {k: np.log(len(tokens_corpus) / v) for k, v in idf_dict.items()}

    def get_words(self, texts_corpus: List[str]) -> List[str]:
        tokens_corpus = [self.tokenizer(text) for text in texts_corpus]
        tf, idf = self.get_tf(tokens_corpus), self.get_idf(tokens_corpus)
        tf_idf = {token: tf[token] * idf[token] for token in tf}
        tf_idf = dict(sorted(tf_idf.items(), key=lambda item: item[1], reverse=True))
        return list(tf_idf.keys())[:self.n]

    def handle_dataloader(self, dataloader: Dataloader, corpus_type: str = "summary"):
        for version in dataloader.versions:
            issues = dataloader.get_issues_by_version(version)
            if corpus_type == "summary":
                top_words = self.get_words([issue.summary for issue in issues])
            elif corpus_type == "description":
                top_words = self.get_words([issue.description for issue in issues])
            else:
                raise ValueError("Wrong corpus_type value!")

            print(f"Версия: {version}")
            print(f"Top-{self.n} words:")
            print(*top_words, sep=', ')
            print()
