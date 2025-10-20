# this file is for reading price data. in current implementation it is reading the data from a csv file. it can do API call or database query

import os
from typing import List

import pandas as pd

from config import PRICES_FILE, DATE_COLUMN_NAME


def read_prices() -> pd.DataFrame:
    # here the logic can change so in the future it can do API call or database query
    # or even some caching mechanism
    # it also can load the prices and keep them in memory if needed.
    return read_prices_csv()


def read_prices_csv() -> pd.DataFrame:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, '..', PRICES_FILE)
    df = pd.read_csv(full_path)
    if DATE_COLUMN_NAME in df.columns:
        df[DATE_COLUMN_NAME] = pd.to_datetime(df[DATE_COLUMN_NAME])
    return df


def read_prices_by_stock(stocks: List[str]) -> pd.DataFrame:
    df = read_prices()
    columns_to_keep = [DATE_COLUMN_NAME] + [stock for stock in stocks if stock in df.columns]
    return df[columns_to_keep]
