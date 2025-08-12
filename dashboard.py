import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="WeatherViz Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# URL da API (ajustar conforme deploy)
API_BASE_URL = "http://localhost:8000"

def get_weather_icon(icon_code):
    """Retorna emoji baseado no código do ícone"""
    icon_map = {
        "01d": "☀️", "01n": "🌙",
        "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icon_map.get(icon_code, "🌤️")

def fetch_weather(city):
    """Busca dados do clima na API"""
    try:
        response = requests.get(f"{API_BASE_URL}/weather/{city}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def fetch_history(city):
    """Busca histórico na API"""
    try:
        response = requests.get(f"{API_BASE_URL}/history/{city}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

# Interface principal
st.title("🌤️ WeatherViz Dashboard")
st.markdown("**Sistema de consulta climática com histórico**")

# Sidebar para busca
with st.sidebar:
    st.header("🔍 Buscar Cidade")
    city_input = st.text_input("Digite o nome da cidade:", placeholder="Ex: São Paulo")
    search_button = st.button("Buscar", type="primary")

# Layout principal
if search_button and city_input:
    weather_data = fetch_weather(city_input)
    
    if weather_data:
        # Dados atuais
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"{get_weather_icon(weather_data['icon'])} {weather_data['city']}, {weather_data['country']}")
            st.markdown(f"**{weather_data['description']}**")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🌡️ Temperatura", f"{weather_data['temperature']}°C")
        
        with col2:
            st.metric("🤚 Sensação Térmica", f"{weather_data['feels_like']}°C")
        
        with col3:
            st.metric("💧 Umidade", f"{weather_data['humidity']}%")
        
        with col4:
            st.metric("💨 Vento", f"{weather_data['wind_speed']} m/s")
        
        # Histórico
        st.subheader("📊 Histórico de Consultas")
        history = fetch_history(city_input)
        
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Gráfico de temperatura
            fig_temp = px.line(
                df, 
                x='timestamp', 
                y='temperature',
                title='Histórico de Temperatura',
                labels={'temperature': 'Temperatura (°C)', 'timestamp': 'Data/Hora'}
            )
            fig_temp.update_layout(height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Gráfico de umidade
            col1, col2 = st.columns(2)
            
            with col1:
                fig_humidity = px.bar(
                    df.head(10), 
                    x='timestamp', 
                    y='humidity',
                    title='Últimas 10 Consultas - Umidade'
                )
                st.plotly_chart(fig_humidity, use_container_width=True)
            
            with col2:
                fig_wind = px.scatter(
                    df.head(10), 
                    x='timestamp', 
                    y='wind_speed',
                    title='Últimas 10 Consultas - Vento',
                    labels={'wind_speed': 'Velocidade do Vento (m/s)'}
                )
                st.plotly_chart(fig_wind, use_container_width=True)
        else:
            st.info("Nenhum histórico encontrado para esta cidade.")
    
    else:
        st.error("❌ Cidade não encontrada ou erro na API. Verifique o nome e tente novamente.")

else:
    # Tela inicial
    st.markdown("""
    ### 👋 Bem-vindo ao WeatherViz!
    
    **Como usar:**
    1. Digite o nome de uma cidade na barra lateral
    2. Clique em "Buscar" para ver o clima atual
    3. Visualize gráficos com o histórico de consultas
    
    **Recursos:**
    - 🌡️ Temperatura atual e sensação térmica
    - 💧 Umidade do ar
    - 💨 Velocidade do vento
    - 📊 Gráficos interativos com histórico
    - 🗄️ Armazenamento automático de consultas
    """)

# Footer
st.markdown("---")
st.markdown("**WeatherViz** - Desenvolvido com FastAPI + Streamlit | Dados: OpenWeatherMap")