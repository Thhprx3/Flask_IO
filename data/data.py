import requests
import datetime
import pandas as pd

def get_coin_list():

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map"
    response = requests.get(api_url)
    data = response.json()['data']
    dataframe = pd.DataFrame.from_dict(data)
    df = dataframe.sort_values(by=['rank'])
    active = df.loc[(df["rank"] >= 1) & (df["rank"] <= 50), ["symbol","slug"]]

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


def get_fiat_list():

    api_url = "https://web-api.coinmarketcap.com/v1/fiat/map"
    response = requests.get(api_url)
    data = response.json()['data']
    df = pd.DataFrame.from_dict(data)

    return df

#fiat = USD / slug = BTC / start_date=2022-04-11 / end_date=2022-04-17
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