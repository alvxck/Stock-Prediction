from flask import Flask, request
from distributor import distributor
from threading import BoundedSemaphore

max_connections = 5
access = BoundedSemaphore(value=max_connections)

app = Flask(__name__)

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

    Send `GET` request to ".../api/get_stock_prediction"
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
    if not access.acquire(blocking=False):
        res = {
            'status': 'error',
            'error': 'Too many requests. Please try again in a few seconds.'
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
        access.release()


if __name__ == '__main__':
    app.run()
