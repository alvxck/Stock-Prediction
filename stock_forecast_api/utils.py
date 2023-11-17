import os
import yfinance as yf



def check_ticker(ticker):
    """
    Checks if an asset already exists in models.
    Checks if an asset is available via the Yahoo Finance API.

    :param ticker: 
    :type ticker: str
    :rtype None
    """

    if (os.path.exists(f'models/{ticker}-seq')):
        raise ValueError(f'{ticker} already exists in models')
    
    if(len(yf.Ticker(ticker).history(period='7d', interval='1d')) > 0):
        raise ValueError(f'{ticker} is not available via Yahoo Finance API')
