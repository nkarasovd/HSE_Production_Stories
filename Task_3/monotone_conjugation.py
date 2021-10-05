from typing import List, Tuple

from scipy.stats import rankdata, pearsonr


class MonotoneConjugationTest:
    @staticmethod
    def _read_data(data_path: str) -> List[List[float]]:
        with open(data_path, 'r') as raw_data:
            return [list(map(float, pair.split())) for pair in raw_data.readlines()]

    @staticmethod
    def _calculate_ranks(data: List[List[float]], axis: int) -> List[float]:
        ranks = rankdata([pair[axis] for pair in data], method="average")
        ranks = [max(ranks) - rank + 1 for rank in ranks]
        return ranks

    @staticmethod
    def _save(data_path: str, diff: int, err: int, conjugation_measure: float):
        with open(data_path, 'w') as data_out:
            data_out.write(' '.join(map(str, [diff, err, conjugation_measure])))

    @staticmethod
    def _calculate_values(ranks: List[float]) -> Tuple[int, int, float]:
        n, p = len(ranks), round(len(ranks) / 3.0)

        r_1, r_2 = sum(ranks[:p]), sum(ranks[-p:])
        diff = int(round(r_1 - r_2))

        err = int(round((n + 0.5) * (p / 6.0) ** 0.5))
        conjugation_measure = round(diff / (p * (n - p)), 2)

        return diff, err, conjugation_measure

    @staticmethod
    def _compare_with_correlation_coefficient(data: List[List[float]], conjugation_measure: float):
        r = pearsonr([pair[0] for pair in data], [pair[1] for pair in data])[0]
        print(f"{'Correlation coefficient:':<25} {round(r, 2)}")
        print(f"{'Conjugation measure:':<25} {conjugation_measure}")

    def test(self, data_path_in: str, data_path_out: str,
             axis: int = 0, compare_with_pearson: bool = True):
        data = self._read_data(data_path_in)

        if len(data) < 9:
            raise ValueError("The number of examples is less than 9!")

        data.sort(key=lambda x: (x[axis], x[1 - axis]))
        ranks = self._calculate_ranks(data, 1 - axis)
        diff, err, conjugation_measure = self._calculate_values(ranks)

        if compare_with_pearson:
            self._compare_with_correlation_coefficient(data, conjugation_measure)

        self._save(data_path_out, diff, err, conjugation_measure)
