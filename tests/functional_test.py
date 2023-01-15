import pytest
from training.functional import functional


@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_functional(ticker):
    forecasted_data, rate = functional(ticker)

    pass