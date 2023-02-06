from pydantic import BaseModel

class ForecastReq(BaseModel):
    key: str
    ticker: str
    period: int

class TrainReq(BaseModel):
    key: str
    ticker: str
    