import pytest

from distributor import distributor

@pytest.mark.parametrize('ticker, period', [
    ('SPY', 1),
    ('SPY', 7),
    ('FB', 1),
    ('FB', 7),
    ('AAPL', 1),
    ('AAPL', 7),
])
def test_distributor(ticker, period):
    forecasted_data, rate = distributor(ticker, period)

    pass