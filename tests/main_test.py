import pytest

@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_app_pass():
    pass

@pytest.mark.parametrize('ticker', ['SPY', 'FB', 'AAPL'])
def test_app_fail():
    pass
