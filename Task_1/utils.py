from typing import Tuple

import numpy as np
import pandas as pd


def get_data(train_path_1: str = 'data/train01.csv', train_path_2: str = 'data/train02.csv',
             test_path: str = 'data/test.csv',
             sep=';') -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_1 = pd.read_csv(filepath_or_buffer=train_path_1, sep=sep)
    train_2 = pd.read_csv(filepath_or_buffer=train_path_2, sep=sep)
    test = pd.read_csv(filepath_or_buffer=test_path, sep=sep)
    
    return train_1, train_2, test


def drop_id(data_1: pd.DataFrame, data_2: pd.DataFrame,
            data_3: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return data_1.drop(columns = ['id']), data_2.drop(columns = ['id']), data_3.drop(columns = ['id'])


def transform_columns_8_9(data: pd.DataFrame):
    data.loc[:, 'x8'] = data['x8'].apply(lambda x: eval(x.replace('nan', 'None').replace('\n ', ',').replace(' ', ','))).copy()
    data.loc[:, 'x9'] = data['x9'].apply(lambda x: eval(x.replace('nan', 'None').replace('\n ', ',').replace(' ', ','))).copy()


def transform_columns_10_42(data: pd.DataFrame, nan_count : int = 4):
    for column_num in range(10, 43):
        def foo(x):
            if x.count('nan') > nan_count:
                return pd.NA
            return x

        def foo_2(x):
            if x is pd.NA:
                return x
            return eval(x.replace('nan', 'None'))

        column = 'x' + str(column_num)
        data[column] = data[column].apply(lambda x: foo(x))
        data[column] = data[column].apply(lambda x: foo_2(x))


def transform_date(data: pd.DataFrame):
    start_size = data.shape[0]
    data = data.dropna(subset=['x2'])
    print(f'Мы удалили {start_size - data.shape[0]} строк')

    mask = data['x2'].apply(lambda x: max(map(int, x.split('.'))))
    print(f'Минимальный год: {min(mask)}, максимальный год: {max(mask)}')

    print('Отсечем года, которые меньше 1990, больше 2020')

    data = data.drop(mask[2020 < mask].index)
    mask = data['x2'].apply(lambda x: max(map(int, x.split('.'))))
    data = data.drop(mask[mask < 1990].index)

    print(f'Минимальная и максимальная даты: {min(data.x2)}, {max(data.x2)}')

    return data


def transform_date_test(data: pd.DataFrame, fill_value: str, date: pd.Timestamp):
    data.x2 = data.x2.fillna(fill_value)
    mask = data['x2'].apply(lambda x: max(map(int, x.split('.'))))
    data.loc[2020 < mask, 'x2'] = fill_value
    data.loc[mask < 2000, 'x2'] = fill_value
    
    data.x2 = pd.to_datetime(data.x2)

    data.x2 = data.x2.apply(lambda x: (date - x).days)
    
    return data


def check_unique(train_1: pd.DataFrame, train_2: pd.DataFrame, test: pd.DataFrame):
    unique_ids_1 = train_1.id.unique()
    unique_ids_2 = train_2.id.unique()
    unique_ids_test = test.id.unique()
    
    print('Train_1')
    print(f'\tВсе id уникальны: {len(unique_ids_1) == train_1.shape[0]}')
    print('Train_2')
    print(f'\tВсе id уникальны: {len(unique_ids_2) == train_2.shape[0]}')
    print('Test')
    print(f'\tВсе id уникальны: {len(unique_ids_test) == test.shape[0]}')


def build_features_train(x):
    z = [i for i in x if i is not None]
    return [min(z), np.mean(z), max(z), 6 - len(z)]


def build_features_test(x, min_1, mean_1, max_1, nan_1):
    if x is pd.NA:
        return [min_1, mean_1, max_1, nan_1]
    
    z = [i for i in x if i is not None]
    
    if z:
        return [min(z), np.mean(z), max(z), 6 - len(z)]
    return [min_1, mean_1, max_1, nan_1]