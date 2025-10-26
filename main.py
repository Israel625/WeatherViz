from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import Query
import uvicorn

from weather_service import WeatherService
from database import WeatherDB
from models import WeatherResponse, WeatherHistory, ErrorResponse, ForecastResponse

app = FastAPI(
    title="WeatherViz API",
    description="API para consulta de dados climáticos com histórico",
    version="1.0.0"
)

# CORS para permitir acesso do Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
weather_service = WeatherService()
db = WeatherDB()

@app.get("/")
def root():
    return {"message": "WeatherViz API - Sistema de consulta climática"}

@app.get("/weather/{city}", response_model=WeatherResponse)
def get_weather(city: str, units: str = "metric", lang: str = "pt_br"):
    try:
        weather_data = weather_service.get_weather(city, units, lang)
        
        # Salvar no banco
        db.save_weather_data(city, weather_data)
        
        return weather_data
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/history/{city}", response_model=List[WeatherHistory])
def get_history(city: str):
    try:
        history = db.get_city_history(city)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao consultar histórico")

@app.get("/forecast/{city}", response_model=ForecastResponse)
def get_forecast(city: str, units: str = "metric", lang: str = "pt_br"):
    try:
        forecast_data = weather_service.get_forecast(city, units, lang)
        return forecast_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/compare")
def compare_cities(cities: str, units: str = "metric", lang: str = "pt_br"):
    """Compara múltiplas cidades. Ex: /compare?cities=São Paulo,Rio de Janeiro,Brasília"""
    try:
        city_list = [city.strip() for city in cities.split(',')]
        if len(city_list) > 5:
            raise HTTPException(status_code=400, detail="Máximo 5 cidades por comparação")
        
        results = []
        for city in city_list:
            try:
                weather_data = weather_service.get_weather(city, units, lang)
                results.append(weather_data)
            except:
                results.append({"city": city, "error": "Cidade não encontrada"})
        
        return {"comparison": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao comparar cidades")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "WeatherViz API"}

# Para Vercel
handler = app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)