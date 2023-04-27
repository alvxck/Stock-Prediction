# Stock Forecast

Stock forecast training model + API

## Overview

Stock Forecast provides utility in estimating stock performance through the use of a sequential neural network. The integrated API allows users to:

* Create a neural network from a specified stock
* Estimate next-day stock performance

## Getting Started

First, setup a virtual environment in the project root directory and activate it.

```
python -m venv venv
venv/scripts/activate
```

Next, install the required packages using the following command:

`pip install -r requirements.txt`

To initialize the API, create a .env file in the root directory of the project and add the following environment variable:

`FLASK_APP = api/app.py`

To start the API, run the following command:

`flask run`

### Training models

Training is done through the `api/train` endpoint which uses a bounded semaphore to limit the number of concurrent training processes. To start a new training process follow these steps:

1. Start the API:

`flask run`

2. Send a POST request to the API with the following JSON body:

```
{
    "ticker": "TICKER",
}
```

3. The API will return a JSON response with the following format:

```
{
    "status": "ok",
    "message": "TICKER model created"
}
```

### Forecasting data

Forecasting is done through the `api/forecast` endpoint which uses a thread lock to limit the number of concurrent forecasting processes. To start a new forecasting process follow these steps:

1. Send a GET request to the API with the following JSON body:

```
{
    "ticker": "TICKER",
}
```

2. The API will return a JSON response with the following format:

```
{
    "status": "ok",
    "forecasted_data": [[$VALUE$]]
    "rate": [[%RATE%]]
}
```


