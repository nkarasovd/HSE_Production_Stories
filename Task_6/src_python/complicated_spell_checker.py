import numpy as np
from scipy.stats import hmean
from spylls.hunspell import Dictionary
from textdistance import damerau_levenshtein, needleman_wunsch, hamming


class ComplicatedSpellChecker:
    def __init__(self, path: str = "en_US"):
        self.dictionary = Dictionary.from_files(path=path)
        self.dist_functions = [damerau_levenshtein.normalized_distance,
                               needleman_wunsch.normalized_distance,
                               hamming.normalized_distance]

    def suggest(self, word: str, count: int = 5):
        candidates = list(self.dictionary.suggester.ngram_suggestions(word, set()))
        distances = [[func(word, candidate) for func in self.dist_functions] for candidate in candidates]

        h_means = [hmean(ds) for ds in distances]
        means = [np.mean(ds) for ds in distances]

        ranks = [(i + j) / 2.0 for i, j in zip(h_means, means)]

        return np.array(candidates)[np.argsort(ranks)][:count]


if __name__ == '__main__':
    sc = ComplicatedSpellChecker()
    print(sc.suggest('doog'))
