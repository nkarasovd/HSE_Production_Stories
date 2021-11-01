import collections
import os
import re
from typing import List, Set, Union


class SimpleSpellChecker:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, dict_path: str = "data/corpus.txt"):
        self.dict_path = dict_path
        self.dict = collections.defaultdict(lambda: 1)

    def fit(self):
        with open(self.dict_path, 'r') as dict_file:
            text = dict_file.read()
            words = re.findall("[a-z]+", text.lower())

            for word in words:
                self.dict[word] += 1

    def _get_words_edit_1_symbol(self, word: str) -> Set[str]:
        n = len(word)

        deletion = [word[0: i] + word[i + 1:] for i in range(n)]
        insertion = [word[0: i] + s + word[i:] for i in range(n) for s in self.alphabet]
        alteration = [word[0: i] + s + word[i + 1:] for i in range(n) for s in self.alphabet]
        transposition = [word[0: i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)]

        return set(deletion + insertion + alteration + transposition)

    def _get_known_words(self, words: Union[List[str], Set[str]]) -> Set[str]:
        return set(word for word in words if word in self.dict)

    def _get_known_words_edit_2_symbol(self, word: str) -> Set[str]:
        edit_1 = self._get_words_edit_1_symbol(word)
        return set(e2 for e1 in edit_1 for e2 in self._get_words_edit_1_symbol(e1) if e2 in self.dict)

    def suggest(self, word: str, count: int = 3):
        candidates = self._get_known_words([word]) or \
                     self._get_known_words(self._get_words_edit_1_symbol(word)) or \
                     self._get_known_words_edit_2_symbol(word) or \
                     [word]
        candidates = sorted(list(candidates), key=lambda w: self.dict[w], reverse=True)
        return candidates[:count]


if __name__ == '__main__':
    os.chdir('/'.join(os.getcwd().split('/')[:-1]))
    sc = SimpleSpellChecker()
    sc.fit()
    print(sc.suggest("doog"))
