import pytest
from app import sequential_forecast, functional_forecast


@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_app_pass():
    pass

@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_app_fail():
    pass
