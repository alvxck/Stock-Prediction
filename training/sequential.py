import sys
import numpy as np
import yfinance as yf
import datetime as dt 
import matplotlib.pyplot as plt

from pandas_datareader import data as pdr
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM


def sequential(ticker):
    '''
    Sequential neural network used for forecasting stock performance.  
    Layers:
        [x3] LSTM
        [x3] Dropout
    Model:
        [optimeser] adam
        [loss] mean_squared_error
        [epochs] 25
        [batch size] 32

    Parameters
    ----------
    ticker : string
        ticker of stock to be forecasted.

    Returns
    -------
    forecasted_data : int
        Forecasted stock price.
    rate : int
        Performance rating compared to previous date.
    
    '''

    yf.pdr_override()
    
    # Load Data
    start = dt.datetime.now() - dt.timedelta(days=5475)
    end = dt.datetime.now()

    data = pdr.get_data_yahoo(ticker, start, end)

    # Pre-process data
    close_data = data['Close'].values.reshape(-1, 1)
    train_len = int(np.ceil(len(close_data) * .95))

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_data)

    # Train model on accuired data
    prediction_days = 60
    train_data = scaled_data[0:int(train_len), :]

    x_train = []
    y_train = []

    for i in range(prediction_days, len(train_data)):
        x_train.append(train_data[i-prediction_days: i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build Model
    model = Sequential()
    model.add(LSTM(units=64, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=64))
    model.add(Dense(32))
    model.add(Dropout(.5))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=10)

    model.save(f'models/{ticker}-seq')

if __name__ == '__main__':
    sequential(ticker=sys.argv[-1])
