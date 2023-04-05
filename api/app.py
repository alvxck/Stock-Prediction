from flask import Flask, request
from threading import Thread, BoundedSemaphore
from api.distributor import distributor
from training.sequential import sequential

app = Flask(__name__)

max_forecast_connections = 5
forecast_access = BoundedSemaphore(value=max_forecast_connections)

@app.route('/api/forecast', methods=['GET'])
def forecast():
    """Forecast stock performance over given period of time.
    Parameters
    ----------
    ticker : string
        Ticker of stock to be projected.
    period : int
        Number of days to forecast up to (inclusive).
    Returns
    -------
    status : string
        Status of request.
    forecasted_data : list
        Array of projected stock performance over given period.
    rate : int
        Performance rating compared to initial date.
    Example
    -------
    Project Apple, Inc. stock performance over the next 30 days.
    Send `GET` request to ".../api/forecast"
        >>> request = {
                "ticker": "AAPL",
                "period": 30
            }
        >>> response = {
                "status": "ok",
                "forecasted_data": {
                    "DATE": $VALUE$,
                    ...
                },
                "rate": %RATE%
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
        period = req['period']

        forecasted_data, rate = distributor(ticker, period)

        res = {
            'status': 'ok',
            'forecasted_data': f"{forecasted_data}",
            'rate': rate,
        }

        return res, 200
    except:
        res = {
            'status': 'error',
            'error': ''
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

        thread = Thread(target=sequential, args=(ticker,))
        thread.start()

        res = {
            'status': 'ok',
            'message': f'{ticker} model created',
        }

        return res, 201
    except:
        res = {
            'status': 'error',
            'error': ''
        }

        return res, 400
    finally:
        train_access.release()


if __name__ == '__main__':
    app.run()
