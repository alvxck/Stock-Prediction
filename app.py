from flask import Flask, request
from analyser import stock_analysis

app = Flask(__name__)

@app.route('/api/get_stock_prediction', methods=['GET'])
def get_stock_prediction():
    """
    Project a given stock performance over a period of time.

    Parameters
    ----------
    ticker : string
        Ticker of stock to be projected.
    period : int
        Time period of stock projection.
    model : string
        Specified compilation model.

    Returns
    -------
    current_data : list
        Array of current stock performance.
    forecasted_data : list
        Array of projected stock performance.

    Example
    -------
    Project Apple, Inc. stock performance over the next 3 months.

    Send `GET` request to ".../api/get_stock_prediction"
        include `ticker` and `period` in json parameters.
        >>> request = {
                "ticker": "AAPL",
                "period": 3,
                "model": "optimized"
            }

    Parse `current_data` and `forecasted_data` returned in json object.
        >>> response["current_data"]
        >>> response["forecasted_data"]
    """

    try:
        req = request.json
        ticker = req['ticker']
        period = req['period']
        model = req['model']

        current_data, forecasted_data = stock_analysis(ticker, period, model)
    except:
        return {
            'status': 'error',
            'error': ''
        }

    return {
        'status': 'ok',
        'current_data': [
            current_data
        ],
        'forecasted_data': [
            forecasted_data
        ],
    }