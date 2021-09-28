from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from tslearn.clustering import TimeSeriesKMeans, KernelKMeans
from tslearn.preprocessing import TimeSeriesResampler
from tslearn.utils import to_time_series_dataset

plt.style.use('seaborn')


def get_train_data(data: pd.DataFrame) -> np.ndarray:
    sessions = data.groupby("session_id")["norm_price"].mean()

    X = []
    for index, count in zip(sessions.index, sessions):
        month = data[data.session_id == index].date.unique()[0].month
        X.append([count, month])

    return np.array(X)


def plot_clusters(data: np.ndarray, labels: np.ndarray):
    fig, ax = plt.subplots()

    colors = list("bgrcmykw")

    for i, x in enumerate(data):
        ax.scatter(x[0], x[1], c=colors[labels[i]])

    plt.title("Кластеризация месячных сессий")
    plt.xlabel("Средняя цена за сессию")
    plt.ylabel("Месяц")

    plt.show()


def get_time_series(data: pd.DataFrame, feature: str) -> List[List[Union[int, float]]]:
    return [value.tolist() for id_, value in data.groupby("session_id")[feature]]


def plot_ts_clusters(cluster_centers: np.ndarray, data: np.ndarray,
                     labels: np.ndarray, n_clusters: int, title: str = None):
    plt.figure(figsize=(20, 20))
    plt.suptitle(title)

    for yi in range(n_clusters):
        plt.subplot((n_clusters + 1) // 2, 2, 1 + yi)

        for xx in data[labels == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.2)

        plt.plot(cluster_centers[yi].ravel(), "r-")
        plt.setp(plt.gca().xaxis.get_majorticklabels(),
                 'rotation', 0)
        plt.title("Cluster %d" % (yi + 1))

    plt.show()


def prepare_data(data: pd.DataFrame, feature: str) -> np.ndarray:
    time_series = get_time_series(data, feature)
    train = to_time_series_dataset(time_series)
    train = TimeSeriesResampler(sz=train.shape[1]).fit_transform(train)
    train = np.nan_to_num(train)

    return train


def use_ts_kmeans(data: np.ndarray, n_clusters: int, metric: str, seed: int):
    model = TimeSeriesKMeans(n_clusters=n_clusters, metric=metric, random_state=seed)
    y_pred = model.fit_predict(data)

    plot_ts_clusters(model.cluster_centers_, data, y_pred, n_clusters)


def use_general_kmeans(data: pd.DataFrame, n_clusters: int):
    X = get_train_data(data)
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    plot_clusters(X, kmeans.labels_)


def use_kernel_kmeans(data: np.ndarray, n_clusters: int, seed: int):
    gak_km = KernelKMeans(n_clusters=n_clusters,
                          kernel="cosine",
                          random_state=seed)
    y_pred = gak_km.fit_predict(data)

    plt.figure(figsize=(20, 20))

    for yi in range(n_clusters):
        plt.subplot((n_clusters + 1) // 2, 2, 1 + yi)
        for xx in data[y_pred == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.2)
        plt.title("Cluster %d" % (yi + 1))

    plt.tight_layout()
    plt.show()
