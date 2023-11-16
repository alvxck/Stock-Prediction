import os
import yfinance as yf



def check_ticker(ticker):
    """
    Checks if an asset already exists in models.
    Checks if an asset is available via the Yahoo Finance API.

    :
    :
    """

    exists = os.path.exists(f'models/{ticker}-seq')
    valid = len(yf.Ticker(ticker).history(period='7d', interval='1d')) > 0

    return exists, valid


def save_ml_model():
    """
    """
    return None