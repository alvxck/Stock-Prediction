import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt 

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
    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2023, 1, 1)

    data = pdr.get_data_yahoo(ticker, start, end)

    # Pre-process Data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    prediction_days = 60

    x_train = []
    y_train = []

    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build Model
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.05))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.05))
    model.add(LSTM(units=50))
    model.add(Dropout(0.05))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)


    # Test Accuracy-----------------------------------------------------------
    test_start = dt.datetime(2022, 10, 1)
    test_end = dt.datetime.now()

    test_data = pdr.get_data_yahoo(ticker, test_start, test_end)

    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)

    x_test = []

    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)

    plt.plot(actual_prices, color="black", label="actual")
    plt.plot(predicted_prices, color="red", label="predicted")
    plt.title("Price")
    plt.xlabel("Time")
    plt.ylabel("Share Price")
    plt.legend()
    plt.show()

sequential("SPY")
