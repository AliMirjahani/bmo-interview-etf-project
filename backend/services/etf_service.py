from typing import List, Dict, Tuple
import pandas as pd

from config import DATE_COLUMN_NAME
from exceptions import StockPriceNotFoundError
from services.etf_price_service import read_prices_by_stock


def calculate_etf_data(etf: pd.DataFrame, top_holdings_count: int) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    stocks = etf['name'].tolist()
    prices = read_prices_by_stock(stocks)
    for stock in stocks:
        if stock not in prices.columns:
            raise StockPriceNotFoundError(stock)

    etf_prices = []
    constituents = []
    holdings_by_value = []
    for index, row in prices.iterrows():
        date = row[DATE_COLUMN_NAME].strftime('%Y-%m-%d')
        price = 0.0
        for _, stock_row in etf.iterrows():
            stock_name = stock_row['name']
            weight = stock_row['weight']
            last_price = row[stock_name]
            price += weight * last_price

        etf_prices.append({'date': date, 'price': round(price, 2)})

    latest_date_idx = prices[DATE_COLUMN_NAME].idxmax()
    latest_prices_row = prices.loc[latest_date_idx]

    for _, stock_row in etf.iterrows():
        stock_name = stock_row['name']
        weight = stock_row['weight']
        last_price = latest_prices_row[stock_name]
        holding_size = weight * last_price

        holdings_by_value.append({
            'name': stock_name,
            'holding_size': round(holding_size, 3)
        })
        constituents.append({
            'name': stock_name,
            'weight': weight,
            'price': round(last_price, 3)
        })
    holdings_by_value.sort(key=lambda x: x['holding_size'], reverse=True)
    top_holdings = holdings_by_value[:top_holdings_count]
    constituents.sort(key=lambda x: x['name'])

    return constituents, top_holdings, etf_prices
