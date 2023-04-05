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
    valid = len(yf.Ticker(ticker).history(period='7d', interval='1d') > 0)

    return exists, valid



def distributor(ticker, period):
    # Load Data
    yf.pdr_override()

    start = dt.datetime.now() - dt.timedelta(days=5475)
    end = dt.datetime.now()
    data = pdr.get_data_yahoo(ticker, start, end)
    prediction_days = 60
    
    model = load_model(f'models/{ticker}-seq')
    scaler = MinMaxScaler(feature_range=(0,1))

    # Pre-process data
    close_data = data['Close'].values.reshape(-1, 1)
    train_len = int(np.ceil(len(close_data) * .95))

    scaled_data = scaler.fit_transform(close_data)

    # Train model on accuired data
    test_data = scaled_data[train_len - prediction_days:, :]
    x_test = []

    for i in range(prediction_days, len(test_data)):
        x_test.append(test_data[i-prediction_days:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # Create prediction based on previosely trained model
    prediction = model.predict(x_test)
    prediction = scaler.inverse_transform(prediction)

    train = data[:train_len]
    test = data[train_len:]

    test['Prediction'] = prediction
  
    # plt.figure(figsize=(7, 5))
    # plt.plot(train['Close'])
    # plt.plot(test[['Close', 'Prediction']])
    # plt.title('Apple Stock Close Price')
    # plt.xlabel('Date')
    # plt.ylabel('Close')
    # plt.legend(['Train', 'Test', 'Prediction'])

    # plt.show()

    return print(test['Prediction'])



# distributor("AAPL", 30)

    # # Calculate rate
    # actual = data['Close'][-1:].values
    # rate = (prediction / actual)-1

    # if rate > 0:
    #     return prediction, f'+{rate}'
    # return prediction, f'{rate}'
