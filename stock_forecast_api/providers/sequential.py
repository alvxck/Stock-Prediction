import sys
import numpy as np
import yfinance as yf
import datetime as dt 

from pandas_datareader import data as pdr
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, LSTM
from stock_forecast_api.models import TickerInput


def distributor(ticker: TickerInput) -> tuple:
    """
    Distributes the sequential neural network to the API.

    :param ticker:
    :type ticker: TickerInput
    :rtype tuple:
    """
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


def sequential(ticker: TickerInput) -> None:
    '''
    Sequential neural network used for forecasting stock performance.  
    Layers:
        [x3] LSTM
        [x3] Dropout
    Model:
        [optimeser] adam
        [loss] mean_squared_error
        [epochs] 10
        [batch size] 32

    :param ticker:
    :type ticker: TickerInput
    :rtype None    
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
