from flask import Flask, request
from threading import Thread, BoundedSemaphore
from api.distributor import check_ticker, distributor 
from training.sequential import sequential

app = Flask(__name__)

max_forecast_connections = 5
forecast_access = BoundedSemaphore(value=max_forecast_connections)

@app.route('/api/forecast', methods=['GET'])
def forecast():
    """Forecast next-day stock performance.
    Parameters
    ----------
    ticker : string
        Ticker of stock to be projected.
    Returns
    -------
    status : string
        Status of request.
    forecasted_data : float
        Estimated next-day value of stock.
    rate : int
        Performance rating compared to previos day.
    Example
    -------
    Project Apple, Inc. stock performance.
    Send `GET` request to ".../api/forecast"
        >>> request = {
                "ticker": "AAPL",
            }
        >>> response = {
                "status": "ok",
                "forecasted_data": [[$VALUE$]]
                "rate": [[%RATE%]]
            }
    """
    if not forecast_access.acquire(blocking=False):
        res = {
            'status': 'error',
            'message': 'Too many requests. Please try again in a few seconds.'
        }
        
        return res, 429
    
    try:
        req = request.json
        ticker = req['ticker']

        exists, valid = check_ticker(ticker)

        if not valid:
            raise Exception(f'{ticker} is not a valid ticker.')

        if not exists:
            raise Exception(f'{ticker} model does not exist. Plase train model first.')

        forecasted_data, rate = distributor(ticker)

        res = {
            'status': 'ok',
            'forecasted_data': f'{forecasted_data}',
            'rate': rate,
        }

        return res, 200
    
    except Exception as e:
        res = {
            'status': 'error',
            'error': e.args[0]
        }

        return res, 400
    
    finally:
        forecast_access.release()


max_train_connections = 1
train_access = BoundedSemaphore(value=max_train_connections)
        
@app.route('/api/train', methods=['POST'])
def train():
    """Create sequential neural network model for a provided stock.
    Parameters
    ----------
    ticker : string
        Ticker of stock to be projected.
    Returns
    -------
    status : string
        Status of request.
    message : string
        Information about request.
    Example
    -------
    Create a model for Apple, Inc.
    Send `POST` request to ".../api/train"
        >>> request = {
                "ticker": "AAPL",
            }
        >>> response = {
                "status": "ok",
                "message": "AAPL model created"
            }
    """
    if not train_access.acquire(blocking=False):
        res = {
            'status': 'error',
            'message': 'Too many requests. Please try again in a few seconds.'
        }
        
        return res, 429
    
    try:
        req = request.json
        ticker = req['ticker']

        exists, valid = check_ticker(ticker)

        if not valid:
            raise Exception(f'{ticker} is not a valid ticker.')

        if exists:
            raise Exception(f'{ticker} model already exists.')
        
        training_thread = Thread(target=sequential, args=(ticker,))
        training_thread.start()

        res = {
            'status': 'ok',
            'message': f'{ticker} model created',
        }

        return res, 201
    
    except Exception as e:
        res = {
            'status': 'error',
            'error': e.args[0]
        }

        return res, 400
    finally:
        train_access.release()


if __name__ == '__main__':
    app.run()
