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
        >>> request =  {
                "ticker": "AAPL",
                "period": "3"
            }

    Parse `current_data` and `forecasted_data` returned in json object.
        >>> response["current_data"]
        >>> response["forecasted_data"]
    """

    # Recieve ticker and time period from user.
    try:
        req = request.json
        ticker = req['ticker']
        period = req['period']

    # Return error if any parameters fail.
    except:
        return {
            'status': 'error',
            'error': ''
        }
    
    # Run neural network analysis on provided ticker over provided time period.
    try: 
        current_data, forecasted_data = stock_analysis(ticker, period)

    # Return error if the ticker does not exist.
    except ValueError:
        pass

    # Return error if the time period exceedes allowable input.
    except ValueError:
        pass

    # Return error if neural network times out.
    except:
        pass

    # Return stock prediction data.
    return {
        'status': 'ok',
        'current_data': [
            current_data
        ],
        'forecasted_data': [
            forecasted_data
        ],
    }