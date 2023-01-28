import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from threading import Thread, BoundedSemaphore
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from pandas_datareader import data as pdr


distributor_semaphore = BoundedSemaphore(value=5)

def distributor(ticker, period):
    global distributor_semaphore
    distributor_semaphore.acquire()

    yf.pdr_override()


    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()
    data = pdr.get_data_yahoo(ticker, start, end)
    prediction_days = 365


    model = load_model(f'models/{ticker}-seq')
    scaler = MinMaxScaler(feature_range=(0,1))
    scaler.fit_transform(data['Close'].values.reshape(-1, 1))

    test_start = dt.datetime.now() - dt.timedelta(days=365)
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

    # Predict next day
    real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs) + 1, 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    print(f'Prediction: {prediction}')

    distributor_semaphore.release()

    # return forecasted_data, rate

distributor_thread = Thread(target=distributor, args=('SPY', 60))
distributor_thread.start()
