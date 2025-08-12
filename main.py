from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from weather_service import WeatherService
from database import WeatherDB
from models import WeatherResponse, WeatherHistory, ErrorResponse

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
def get_weather(city: str):
    try:
        weather_data = weather_service.get_weather(city)
        
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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "WeatherViz API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)