from flask import Flask, request
from distributer import distributer

app = Flask(__name__)

@app.route('/api/single_day_forecast', methods=['GET'])
def sequential_forecast():
    """
    Forecast stock performance over a single day.

    Parameters
    ----------
    ticker : string
        Ticker of stock to be projected.

    Returns
    -------
    status : string
        Status of request.
    forecasted_data : int
        Projected stock price.
    rate : int
        Performance rating compared to previous date.

    Example
    -------
    Project Apple, Inc. stock performance tomorrow.

    Send `GET` request to ".../api/single_day_forecast"
        >>> request = {
                "ticker": "AAPL",
            }

        >>> response = {
                "status": "ok",
                "forecasted_data": $VALUE$,
                "rate": %RATE%
            }
    """

    try:
        req = request.json
        ticker = req['ticker']

        forecasted_data, rate = distributer(ticker, period=1, model='sequential')
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

@app.route('/api/multi_day_forecast', methods=['GET'])
def functional_forecast():
    """
    Forecast stock performance over multiple days.

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

        forecasted_data, rate = distributer(ticker, period, model='functional')
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