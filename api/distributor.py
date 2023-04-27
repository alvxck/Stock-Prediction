import os
import numpy as np
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from pandas_datareader import data as pdr


def check_ticker(ticker):
    """
    Checks if an asset already exists in models.
    Checks if an asset is available via the Yahoo Finance API.
    """

    exists = os.path.exists(f'models/{ticker}-seq')
    valid = len(yf.Ticker(ticker).history(period='7d', interval='1d')) > 0

    return exists, valid


def distributor(ticker):
    # Pre-process data
    yf.pdr_override()

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()
    data = pdr.get_data_yahoo(ticker, start, end)
    prediction_days = 60

    model = load_model(f'models/{ticker}-seq')
    scaler = MinMaxScaler(feature_range=(0,1))

    model_inputs = data['Close'][-prediction_days*10:].values.reshape(-1, 1)
    model_inputs = scaler.fit_transform(model_inputs)

    # Predict next day
    projection_sample = [model_inputs[len(model_inputs) - prediction_days:len(model_inputs), 0]]
    projection_sample = np.array(projection_sample)
    projection_sample = np.reshape(projection_sample, (projection_sample.shape[0], projection_sample.shape[1], 1))

    prediction = model.predict(projection_sample)
    prediction = scaler.inverse_transform(prediction)

    # Calculate rate
    actual = data['Close'][-1:].values
    rate = (prediction / actual)-1

    if rate > 0:
        return prediction, f'+{rate}'
    return prediction, f'{rate}'
