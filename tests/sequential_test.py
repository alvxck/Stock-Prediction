import pytest
from models.sequential import sequential

@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_sequential(ticker):
    forecasted_data, rate = sequential(ticker)

    pass
