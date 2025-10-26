from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    icon: str

class WeatherHistory(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: int
    wind_speed: float
    feels_like: float
    description: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    message: str

class ForecastItem(BaseModel):
    datetime: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    icon: str

class ForecastResponse(BaseModel):
    city: str
    country: str
    forecasts: List[ForecastItem]