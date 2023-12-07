# Stock Forecast

Stock forecast training model + API

## Overview

Stock Forecast provides utility in estimating stock performance through the use of a sequential neural network. The integrated API allows users to:

* Create a neural network from a specified stock
* Estimate next-day stock performance

## Getting Started

First, setup a virtual environment (v3.11.3) in the project root and activate it.

```
py -3.11.3 -m venv venv
venv/scripts/activate
```

Next, install the required packages using the following command:

`pip install -r requirements.txt`

To start the API, run the following command from the root:

`uvicorn stock_forecast_api.app:app --reload`

### Training models

Training is done through the `api/sequential/train` endpoint which uses a process queue to process concurrent training requests in order. To start a new training process follow these steps:

1. Start the API:

`uvicorn stock_forecast_api.app:app --reload`

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

Forecasting is done through the `api/sequential/forecast` endpoint. To start a new forecasting process follow these steps:

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


