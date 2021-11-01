import os
from typing import Tuple

from tqdm import tqdm

from src_python.complicated_spell_checker import ComplicatedSpellChecker


def test(model, path: str = "data/test.txt") -> Tuple[float, float, float]:
    acc_1, acc_3, acc_5 = 0, 0, 0

    with open(path, 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            words = line.split()
            a, b = words[0], ' '.join(words[1:])
            preds = model.suggest(a, count=5)

            if b in preds[:1]:
                acc_1 += 1
                acc_3 += 1
                acc_5 += 1
            elif b in preds[:3]:
                acc_3 += 1
                acc_5 += 1
            elif b in preds[:5]:
                acc_5 += 1

        return acc_1 / len(lines), acc_3 / len(lines), acc_5 / len(lines)


if __name__ == '__main__':
    os.chdir('/'.join(os.getcwd().split('/')[:-1]))
    sc = ComplicatedSpellChecker()
    acc_1, acc_3, acc_5 = test(sc)
    print(f"Acc@1 = {round(acc_1, 2)} | Acc@3 = {round(acc_3, 2)} | Acc@5 = {round(acc_5, 2)}")
