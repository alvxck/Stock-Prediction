import os
import yfinance as yf

from queue import Queue
from asyncio import get_event_loop

from stock_forecast_api.models import TickerInput
from stock_forecast_api.providers.sequential import sequential 


ticker_queue: Queue[TickerInput] = Queue()

async def process_ticker_queue():
    """
    Process the ticker queue and run the sequential neural network training
    in order of tickers received from the API.

    :rtype None
    """
    bg_process = get_event_loop()
    while True:
        ticker: TickerInput = await bg_process.run_in_executor(None, ticker_queue.get())
        await bg_process.run_in_executor(None, sequential, ticker) 
        ticker_queue.task_done()    

def check_ticker(ticker: TickerInput) -> None:
    """
    Checks if an asset already exists in models.
    Checks if an asset is available via the Yahoo Finance API.

    :param ticker: 
    :type ticker: TickerInput
    :rtype None
    """

    if (os.path.exists(f'models/{ticker}-seq')):
        raise ValueError(f'{ticker} already exists in models')
    
    if(len(yf.Ticker(ticker).history(period='7d', interval='1d')) > 0):
        raise ValueError(f'{ticker} is not available via Yahoo Finance API')