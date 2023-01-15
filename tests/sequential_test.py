import pytest
from training.sequential import sequential

@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_sequential(ticker):
    forecasted_data, rate = sequential(ticker)

    pass
