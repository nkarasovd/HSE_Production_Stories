import datetime as dt
import sqlite3
from typing import Tuple

import pandas as pd


def load_data(database_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    con = sqlite3.connect(database_path)

    trading_session_df = pd.read_sql_query("SELECT * from Trading_session", con)
    chart_data_df = pd.read_sql_query("SELECT * from Chart_data", con)

    con.close()

    trading_session_df = trading_session_df.rename(columns={"id": "session_id"})
    chart_data_df = chart_data_df.rename(columns={"id": "chart_id"})
    chart_data_df['time'] = pd.to_datetime(chart_data_df.time, format='%H:%M:%S').dt.time

    return trading_session_df, chart_data_df


def print_data_info(trading_session_df: pd.DataFrame, chart_data_df: pd.DataFrame):
    print(f"{'Размер датафрейма trading_session_df:':<50} {trading_session_df.shape}")
    print(f"{'Размер датафрейма chart_data_df:':<50} {chart_data_df.shape}\n")

    print(f"{'Число уникальных session_id в trading_session_df:':<50} {trading_session_df.session_id.nunique()}")
    print(f"{'Число уникальных session_id в chart_data_df:':<50} {chart_data_df.session_id.nunique()}\n")

    print(f"{'Число уникальных chart_id в chart_data_df:':<50} {chart_data_df.chart_id.nunique()}")
    print(f"{'Число уникальных deal_id в chart_data_df:':<50} {chart_data_df.deal_id.nunique()}")


def compare_session_id(trading_session_df: pd.DataFrame, chart_data_df: pd.DataFrame):
    a = trading_session_df.session_id.unique()
    b = chart_data_df.session_id.unique()
    print(f"Число уникальных session_id в trading_session_df: {len(a)}")
    print(f"Число уникальных session_id в chart_data_df: {len(b)}")
    print(f"Число общих сессий: {len(set(a).intersection(set(b)))}")


def get_dataframes(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    mask = data.trading_type == sorted(data.trading_type.unique())[0]
    daily_df = data[mask].copy()
    monthly_df = data[~mask].copy()

    return daily_df, monthly_df


def create_columns(row: pd.Series) -> pd.Timestamp:
    date = pd.to_datetime(row.date)
    return date + dt.timedelta(hours=row.time.hour, minutes=row.time.minute, seconds=row.time.second)


def add_columns(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, "global_date"] = data.apply(lambda row: create_columns(row), axis=1)
    data.loc[:, "date"] = data.loc[:, "global_date"].apply(lambda x: x.date())
    data.loc[:, "hour"] = data.loc[:, "time"].apply(lambda x: x.hour)
    data.loc[:, "minute"] = data.loc[:, "time"].apply(lambda x: x.minute)
    data.loc[:, "second"] = data.loc[:, "time"].apply(lambda x: x.second)
    data.loc[:, "norm_price"] = data.groupby("session_id")["price"].transform(lambda x: (x - x.mean()) / (x.std() + 1))
    data.loc[:, "norm_lot_size"] = data.groupby("session_id")["lot_size"].transform(
        lambda x: (x - x.mean()) / (x.std() + 1))
    return data


def delete_small_sessions(data: pd.DataFrame, treshold: int = 15) -> pd.DataFrame:
    mask = data.session_id.value_counts()
    return data[data.session_id.isin(mask[mask > treshold].index)]
