import requests
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    def get_weather(self, city: str, units: str = "metric", lang: str = "pt_br") -> Dict:
        if not self.api_key:
            raise ValueError("API key não configurada")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 404:
            raise ValueError(f"Cidade '{city}' não encontrada")
        elif response.status_code != 200:
            raise ValueError("Erro ao consultar API do clima")
        
        data = response.json()
        
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"], 1),
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }
    
    def get_forecast(self, city: str, units: str = "metric", lang: str = "pt_br") -> Dict:
        if not self.api_key:
            raise ValueError("API key não configurada")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": lang
        }
        
        response = requests.get(self.forecast_url, params=params)
        
        if response.status_code == 404:
            raise ValueError(f"Cidade '{city}' não encontrada")
        elif response.status_code != 200:
            raise ValueError("Erro ao consultar previsão do tempo")
        
        data = response.json()
        
        forecasts = []
        for item in data["list"][:40]:  # 5 dias, 8 previsões por dia
            forecasts.append({
                "datetime": item["dt_txt"],
                "temperature": round(item["main"]["temp"], 1),
                "feels_like": round(item["main"]["feels_like"], 1),
                "humidity": item["main"]["humidity"],
                "wind_speed": round(item["wind"]["speed"], 1),
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"]
            })
        
        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": forecasts
        }