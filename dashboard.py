import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import numpy as np
import io

# Configuração da página
st.set_page_config(
    page_title="WeatherViz Dashboard",
    page_icon="☁️",
    layout="wide"
)

# CSS simplificado
st.markdown("""
<style>
.metric-card { 
    border: 1px solid #ddd;
    padding: 1rem; 
    border-radius: 8px; 
    text-align: center;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# URL da API
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

# Função removida para melhor performance

def fetch_weather(city, units="metric", lang="pt_br"):
    """Busca dados do clima na API"""
    try:
        params = {"units": units, "lang": lang}
        response = requests.get(f"{API_BASE_URL}/weather/{city}", params=params)
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

def fetch_forecast(city, units="metric", lang="pt_br"):
    """Busca previsão de 5 dias na API"""
    try:
        params = {"units": units, "lang": lang}
        response = requests.get(f"{API_BASE_URL}/forecast/{city}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def fetch_comparison(cities, units="metric", lang="pt_br"):
    """Compara múltiplas cidades"""
    try:
        cities_str = ','.join(cities)
        params = {"units": units, "lang": lang}
        response = requests.get(f"{API_BASE_URL}/compare?cities={cities_str}", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Interface principal
st.title("WeatherViz Dashboard")
st.markdown("**Sistema profissional de consulta climática com histórico**")

# Sidebar para busca
with st.sidebar:
    st.header("Configurações")
    
    # Configurações
    units = st.selectbox("Unidade de Temperatura:", ["Celsius", "Fahrenheit"])
    lang = st.selectbox("Idioma:", ["Português", "English", "Español"])
    
    st.divider()
    st.header("Buscar Cidade")
    
    # Abas para diferentes funcionalidades
    tab = st.selectbox("Escolha a funcionalidade:", 
                      ["Clima Atual", "Previsão 5 Dias", "Comparar Cidades"])
    
    if tab == "Clima Atual" or tab == "Previsão 5 Dias":
        city_input = st.text_input("Digite o nome da cidade:", placeholder="Ex: São Paulo")
        search_button = st.button("Buscar", type="primary")
    
    elif tab == "Comparar Cidades":
        st.markdown("**Digite até 5 cidades (uma por linha):**")
        cities_input = st.text_area("Cidades:", placeholder="São Paulo\nRio de Janeiro\nBrasília", height=100)
        compare_button = st.button("Comparar", type="primary")

# Configurar parâmetros baseado nas seleções
api_units = "metric" if units == "Celsius" else "imperial"
lang_map = {"Português": "pt_br", "English": "en", "Español": "es"}
api_lang = lang_map[lang]
temp_unit = "°C" if units == "Celsius" else "°F"

# Layout principal
if tab == "Clima Atual" and search_button and city_input:
    weather_data = fetch_weather(city_input, api_units, api_lang)
    
    if weather_data:
        # Dados atuais
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"{weather_data['city']}, {weather_data['country']}")
            st.write(f"**{weather_data['description']}**")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Temperatura", f"{weather_data['temperature']}{temp_unit}")
        with col2:
            st.metric("Sensação", f"{weather_data['feels_like']}{temp_unit}")
        with col3:
            st.metric("Umidade", f"{weather_data['humidity']}%")
        with col4:
            st.metric("Vento", f"{weather_data['wind_speed']} m/s")
        
        # Histórico
        st.subheader("Histórico de Consultas")
        history = fetch_history(city_input)
        
        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Botão de exportar histórico
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Baixar Histórico (CSV)",
                data=csv_data,
                file_name=f"historico_{city_input.replace(' ', '_')}.csv",
                mime="text/csv"
            )
            
            # Análise dos dados para insights
            temp_max = df['temperature'].max()
            temp_min = df['temperature'].min()
            temp_avg = df['temperature'].mean()
            
            # Gráfico de temperatura
            fig_temp = px.line(
                df, 
                x='timestamp', 
                y='temperature',
                title=f'Temperatura em {city_input} (Máx: {temp_max:.1f}{temp_unit}, Mín: {temp_min:.1f}{temp_unit})',
                color_discrete_sequence=['#ff6b6b']
            )
            
            # Adicionar linha de média
            fig_temp.add_hline(
                y=temp_avg, 
                line_dash="dash", 
                line_color="orange",
                annotation_text=f"Média: {temp_avg:.1f}{temp_unit}"
            )
            
            fig_temp.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            fig_temp.update_traces(line=dict(width=3))
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Gráfico de umidade
            col1, col2 = st.columns(2)
            
            with col1:
                humidity_avg = df.head(10)['humidity'].mean()
                fig_humidity = px.bar(
                    df.head(10), 
                    x='timestamp', 
                    y='humidity',
                    title=f'Umidade - Últimas 10 consultas (Média: {humidity_avg:.0f}%)',
                    color='humidity',
                    color_continuous_scale='Blues'
                )
                
                # Adicionar zona de conforto
                fig_humidity.add_hrect(
                    y0=40, y1=60, 
                    fillcolor="green", opacity=0.1,
                    annotation_text="Zona Ideal"
                )
                
                fig_humidity.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_humidity, use_container_width=True)
            
            with col2:
                wind_max = df.head(10)['wind_speed'].max()
                fig_wind = px.scatter(
                    df.head(10), 
                    x='timestamp', 
                    y='wind_speed',
                    title=f'Vento - Últimas 10 consultas (Máx: {wind_max:.1f} m/s)',
                    color='wind_speed',
                    size='wind_speed'
                )
                
                # Linha indicativa de vento forte
                if wind_max > 5:
                    fig_wind.add_hline(
                        y=10, line_dash="dash", line_color="red",
                        annotation_text="Vento Forte"
                    )
                
                fig_wind.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_wind, use_container_width=True)
        else:
            st.info("Nenhum histórico encontrado para esta cidade.")
    
    else:
        st.error("❌ Cidade não encontrada ou erro na API. Verifique o nome e tente novamente.")

elif tab == "Previsão 5 Dias" and search_button and city_input:
    forecast_data = fetch_forecast(city_input, api_units, api_lang)
    
    if forecast_data:
        st.subheader(f"Previsão de 5 dias - {forecast_data['city']}, {forecast_data['country']}")
        
        # Converter para DataFrame
        df_forecast = pd.DataFrame(forecast_data['forecasts'])
        df_forecast['datetime'] = pd.to_datetime(df_forecast['datetime'])
        df_forecast['date'] = df_forecast['datetime'].dt.date
        
        # Botão de exportar previsão
        csv_forecast = df_forecast.to_csv(index=False)
        st.download_button(
            label="Baixar Previsão (CSV)",
            data=csv_forecast,
            file_name=f"previsao_{city_input.replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        # Análise da previsão
        forecast_max = df_forecast['temperature'].max()
        forecast_min = df_forecast['temperature'].min()
        
        # Gráfico de previsão
        fig_temp_forecast = px.line(
            df_forecast, 
            x='datetime', 
            y='temperature',
            title=f'Previsão 5 dias - {city_input} (Máx: {forecast_max:.1f}{temp_unit}, Mín: {forecast_min:.1f}{temp_unit})',
            color_discrete_sequence=['#4ecdc4']
        )
        
        # Destacar máxima e mínima
        max_point = df_forecast[df_forecast['temperature'] == forecast_max].iloc[0]
        min_point = df_forecast[df_forecast['temperature'] == forecast_min].iloc[0]
        
        fig_temp_forecast.add_scatter(
            x=[max_point['datetime']], y=[max_point['temperature']],
            mode='markers+text', marker=dict(color='red', size=12),
            text=[f'Máx: {forecast_max:.1f}{temp_unit}'], textposition='top center',
            name='Máxima', showlegend=False
        )
        
        fig_temp_forecast.add_scatter(
            x=[min_point['datetime']], y=[min_point['temperature']],
            mode='markers+text', marker=dict(color='blue', size=12),
            text=[f'Mín: {forecast_min:.1f}{temp_unit}'], textposition='bottom center',
            name='Mínima', showlegend=False
        )
        
        fig_temp_forecast.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_temp_forecast.update_traces(line=dict(width=3))
        st.plotly_chart(fig_temp_forecast, use_container_width=True)
        
        # Resumo por dia
        daily_summary = df_forecast.groupby('date').agg({
            'temperature': ['min', 'max', 'mean'],
            'humidity': 'mean',
            'description': 'first'
        }).round(1)
        
        st.subheader("Resumo Diário")
        for date in daily_summary.index:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"{date}", f"{daily_summary.loc[date, ('description', 'first')]}")
            with col2:
                st.metric("Mín/Máx", f"{daily_summary.loc[date, ('temperature', 'min')]}°/{daily_summary.loc[date, ('temperature', 'max')]}°")
            with col3:
                st.metric("Média", f"{daily_summary.loc[date, ('temperature', 'mean')]}{temp_unit}")
            with col4:
                st.metric("Umidade", f"{daily_summary.loc[date, ('humidity', 'mean')]}%")
    else:
        st.error("❌ Erro ao buscar previsão. Verifique o nome da cidade.")

elif tab == "Comparar Cidades" and compare_button and cities_input:
    cities_list = [city.strip() for city in cities_input.split('\n') if city.strip()]
    
    if len(cities_list) > 5:
        st.error("❌ Máximo 5 cidades permitidas")
    elif len(cities_list) < 2:
        st.error("❌ Digite pelo menos 2 cidades")
    else:
        comparison_data = fetch_comparison(cities_list, api_units, api_lang)
        
        if comparison_data:
            st.subheader("Comparação entre Cidades")
            
            # Filtrar cidades válidas
            valid_cities = [city for city in comparison_data['comparison'] if 'error' not in city]
            
            if valid_cities:
                # Criar DataFrame para comparação
                df_comparison = pd.DataFrame(valid_cities)
                
                # Botão de exportar comparação
                csv_comparison = df_comparison.to_csv(index=False)
                st.download_button(
                    label="Baixar Comparação (CSV)",
                    data=csv_comparison,
                    file_name="comparacao_cidades.csv",
                    mime="text/csv"
                )
                
                # Gráficos melhorados
                col1, col2 = st.columns(2)
                
                # Análise comparativa
                hottest_city = df_comparison.loc[df_comparison['temperature'].idxmax(), 'city']
                coldest_city = df_comparison.loc[df_comparison['temperature'].idxmin(), 'city']
                most_humid = df_comparison.loc[df_comparison['humidity'].idxmax(), 'city']
                
                with col1:
                    fig_temp_comp = px.bar(
                        df_comparison, 
                        x='city', 
                        y='temperature',
                        title=f'Temperatura por cidade (Mais quente: {hottest_city})',
                        color='temperature',
                        color_continuous_scale='RdYlBu_r',
                        text='temperature'
                    )
                    fig_temp_comp.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_temp_comp.update_traces(
                        texttemplate='%{text}{}'.format(temp_unit), 
                        textposition='outside'
                    )
                    st.plotly_chart(fig_temp_comp, use_container_width=True)
                
                with col2:
                    fig_humidity_comp = px.bar(
                        df_comparison, 
                        x='city', 
                        y='humidity',
                        title=f'Umidade por cidade (Mais úmido: {most_humid})',
                        color='humidity',
                        color_continuous_scale='Blues',
                        text='humidity'
                    )
                    
                    # Zona de conforto
                    fig_humidity_comp.add_hrect(
                        y0=40, y1=60, 
                        fillcolor="green", opacity=0.1,
                        annotation_text="Zona Ideal"
                    )
                    
                    fig_humidity_comp.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_humidity_comp.update_traces(
                        texttemplate='%{text}%', 
                        textposition='outside'
                    )
                    st.plotly_chart(fig_humidity_comp, use_container_width=True)
                
                # Tabela de comparação
                st.subheader("Tabela Comparativa")
                display_df = df_comparison[['city', 'temperature', 'feels_like', 'humidity', 'wind_speed', 'description']]
                display_df.columns = ['Cidade', f'Temp ({temp_unit})', f'Sensação ({temp_unit})', 'Umidade (%)', 'Vento (m/s)', 'Descrição']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Mostrar erros se houver
            error_cities = [city for city in comparison_data['comparison'] if 'error' in city]
            if error_cities:
                st.warning(f"⚠️ Cidades não encontradas: {', '.join([c['city'] for c in error_cities])}")
        else:
            st.error("❌ Erro ao comparar cidades")

else:
    # Tela inicial
    st.markdown("""
    ### Bem-vindo ao WeatherViz!
    
    **Funcionalidades disponíveis:**
    
    **Clima Atual**
    - Temperatura, umidade e vento em tempo real
    - Histórico de consultas com gráficos
    
    **Previsão 5 Dias**
    - Previsão detalhada hora a hora
    - Resumo diário com temperaturas mín/máx
    
    **Comparar Cidades**
    - Compare até 5 cidades simultaneamente
    - Gráficos comparativos e tabela resumo
    
    **Como usar:**
    1. Escolha uma funcionalidade na barra lateral
    2. Digite o nome da(s) cidade(s)
    3. Clique no botão correspondente
    """)

# Footer
st.markdown("---")
st.markdown("**WeatherViz** - Desenvolvido com FastAPI + Streamlit | Dados: OpenWeatherMap")