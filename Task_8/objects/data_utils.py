from typing import Dict

import numpy as np
import pandas as pd
from gensim.models import CoherenceModel
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from matplotlib import pyplot as plt
from tqdm import tqdm

from models.lda import LDAModel
from objects.tokenizer import Tokenizer


def get_versions(df: pd.DataFrame) -> Dict[str, int]:
    versions = {}

    for vs in df["Affected versions"]:
        if vs is not np.nan:
            for v in vs:
                versions[v] = versions.get(v, 1) + 1

    return versions


def print_info(df: pd.DataFrame):
    print(f"Num examples: {df.shape[0]:>7}")
    print(f"Num features: {df.shape[1]:>6}\n")

    warning, bold, end = "\033[93m", "\033[1m", "\033[0m"
    format_len = max(map(len, df.columns)) + 1

    print("NA ratio stat:")

    for column in df.columns:
        na_ratio = df[column].isna().sum() / df.shape[0]
        if na_ratio >= 0.4:
            print(f"{warning}{bold}\tColumn: {column:>{format_len}}, NA ratio: {round(na_ratio, 5)}{end}")
        else:
            print(f"\tColumn: {column:>{format_len}}, NA ratio: {round(na_ratio, 5)}")


def detect_language(t):
    if t is None:
        return np.nan
    try:
        return detect(t)
    except LangDetectException:
        return np.nan


def plot_versions_bar(data: pd.DataFrame):
    vs = get_versions(data)
    lst = sorted(list(vs.items()), key=lambda x: int(x[0][:4] + x[0][5]))
    v = [x[0] for x in lst]
    k = [x[1] for x in lst]

    plt.figure(figsize=(12, 8))
    plt.bar(v, k)
    plt.xticks(rotation=50)
    plt.xlabel("Versions")
    plt.ylabel("Number of issues")
    plt.tight_layout()
    plt.show()


def grid_search(raw_corpus, grid):
    my_lda = LDAModel(1, Tokenizer(), raw_corpus)

    results = []
    for n in tqdm(grid):
        my_lda.update_num_topics(n)
        results.append(CoherenceModel(my_lda.lda, corpus=my_lda.corpus, coherence="u_mass",
                                      dictionary=my_lda.dicts).get_coherence())

    return results


def plot_coherence_scores(raw_corpus, grid):
    coherence_scores = grid_search(raw_corpus, grid)

    plt.figure(figsize=(12, 8))
    plt.plot(grid, coherence_scores)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence")
    plt.tight_layout()
    plt.show()


def get_top_topics(topics, top_n: int = 10):
    unique_topics, count = np.unique(topics, return_counts=True)
    return unique_topics[np.argsort(-count)][:top_n]
