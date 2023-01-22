import sys
import numpy as np
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
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()

    try: 
        data = pdr.get_data_yahoo(ticker, start, end)
    except:
        print('Invalid ticker. Please try agian.')

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
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=1, batch_size=32)

    model.save(f'models/{ticker}-seq')

if __name__ == '__main__':
    sequential(ticker=sys.argv[-1])
