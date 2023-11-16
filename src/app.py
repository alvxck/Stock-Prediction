from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import sequential_api

app = FastAPI()
app.title = "Stock Forecast"
app.description = "API to forecast next-day stock prices"

api = FastAPI(openapi_prefix="/api")
api.include_router(sequential_api.router, prefix="/sequential")

api.mount("/api", api, name="api")

origins = ["http://localhost:1738"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credential=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/healthcheck")
async def healthcheck():
    """
    Endpoint to verify the API is running
    """
    return {"message": "Stock Forecast API is running..."}

