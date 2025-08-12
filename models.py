from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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