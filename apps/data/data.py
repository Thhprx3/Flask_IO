import requests
import numpy as np
import pandas as pd

#Historical data
#day - price by day (OHLCV), hour - price by hour (OHLCV), minute - price by minute (OHLCV)

def get_data_test(f_symbol, t_symbol, limit=1, aggregate=1):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym={}&tsym={}&limit={}&aggregate={}&allData=true'\
        .format(f_symbol, t_symbol, limit, aggregate)
    response = requests.get(url)
    data = response.json()['Data']['Data']
    df = pd.DataFrame.from_dict(data)
    df['timestamp'] = (pd.to_datetime(df['time'], unit='s'))
    return df