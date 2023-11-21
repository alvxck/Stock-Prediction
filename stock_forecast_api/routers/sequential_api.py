from fastapi import APIRouter
from starlette.responses import JSONResponse

from stock_forecast_api.models import TickerInput
from stock_forecast_api.providers.sequential import distributor
from stock_forecast_api.utils import check_ticker, process_ticker_queue, ticker_queue


router = APIRouter()

router.add_event_handler("startup", process_ticker_queue)

@router.get("/forecast")
async def get_forecast(user_input: TickerInput) -> JSONResponse:
    """
    Use sequential neural network to forecast stock price for next day

    :param user_iput: 
    :type user_input: TickerInput
    :rtype JSONResponse
    """
    check_ticker(ticker=user_input.ticker)
    forecasted_data, rate = distributor(user_input.ticker)

    return JSONResponse({
        'status': 'ok',
        'forecasted_data': f'{forecasted_data}',
        'rate': rate,
    })


@router.post("/train") 
async def post_trian(user_input: TickerInput) -> JSONResponse:
    """
    Train sequential neural network to forecast stock price for next day

    :param user_iput: 
    :type user_input: TickerInput
    :rtype JSONResponse
    """
    check_ticker(ticker=user_input.ticker)
    ticker_queue.put(user_input.ticker)

    return JSONResponse({
        'status': 'ok',
        'message': f'{user_input.ticker} model created'
    })
