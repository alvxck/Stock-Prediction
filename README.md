# Stock Forecast

Stock forecast training model + API

## Overview

Stock Forecast provides utility in estimating stock performance through the use of a sequential neural network. The integrated API allows users to:

* Train sequential neural networks for specified stocks
* Estimate stock performance over a time period
* Generate graphs of the estimated stock performance

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

### Basic Usage
