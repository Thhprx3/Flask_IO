import requests
import datetime
import pandas as pd
import re

def get_coin_list():
    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map"
    response = requests.get(api_url)
    data = response.json()['data']
    dataframe = pd.DataFrame.from_dict(data)
    df = dataframe.sort_values(by=['rank'])
    active = df.loc[(df["rank"] >= 1) & (df["rank"] <= 200), ["symbol","slug"]]
    return active


def get_first_date(symbol):
    coin_list = get_coin_list()
    coin_list['first_historical_data'] = pd.to_datetime(coin_list['first_historical_data']).dt.date
    date = coin_list.loc[(coin_list["symbol"]) == symbol, "first_historical_data"].tolist()
    return date


def convert_symbol_slug(symbol):
    df = get_coin_list()
    slug = df.loc[df['symbol'] == symbol, 'slug'].iloc[0]
    return slug


def get_fiat_list(symbol=None):
    api_url = "https://web-api.coinmarketcap.com/v1/fiat/map"
    response = requests.get(api_url)
    data = response.json()['data']
    df = pd.DataFrame.from_dict(data)
    if symbol is None:
        return df
    else:
        sign = df.loc[df['symbol'] == symbol, 'sign'].iloc[0]
        return sign


def historical_data(fiat, slug, start_date, end_date):
    start_date = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_date = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    slug = convert_symbol_slug(str(slug))
    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={}&slug={}&time_start={}&time_end={}".format(
        fiat, slug, start_date, end_date
    )
    response = requests.get(api_url).json()['data']
    df = pd.json_normalize(response, 'quotes', ['symbol'])
    df.rename(columns=lambda x: x.replace('quote.'+fiat+'.', ''), inplace=True)
    return df


def get_info(symbol):
    api_url = "https://web-api.coinmarketcap.com/v2/cryptocurrency/info?symbol={}".format(
        symbol
    )
    data = requests.get(api_url).json()['data']
    df = pd.json_normalize(data, record_path=symbol)
    df = pd.DataFrame(df)
    info = df[df.columns[0:7]]
    return info


def price_changes(symbol, convert):
    api_url = "https://web-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest?symbol={}&convert={}&time_period=24h".format(
        symbol, convert
    )
    response = requests.get(api_url).json()['data'][symbol.upper()]
    data = pd.json_normalize(response)
    data.rename(columns=lambda x: re.sub(".*(?=\.).","",x), inplace=True)
    df = data[['name','symbol','slug','low','high','open','close','percent_change','price_change']]
    return df