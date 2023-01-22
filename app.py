from flask import Flask, request
from distributor import distributor

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

    try:
        req = request.json
        ticker = req['ticker']
        period = req['period']

        forecasted_data, rate = distributor(ticker, period)
    except:
        return {
            'status': 'error',
            'error': ''
        }
     
    return {
        'status': 'ok',
        'forecasted_data': forecasted_data,
        'rate': rate,
    }