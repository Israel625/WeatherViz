# WeatherViz

Sistema completo de consulta climática com API REST e dashboard interativo.

## Funcionalidades

- **API REST** com FastAPI
- **Dashboard interativo** com Streamlit
- **Histórico de consultas** em SQLite
- **Gráficos dinâmicos** com Plotly
- **Previsão de 5 dias** com gráficos de tendência
- **Comparação entre cidades** (até 5 simultaneamente)
- **Configurações personalizadas** (Celsius/Fahrenheit, idiomas)
- **Exportação de dados** em CSV
- **Deploy em nuvem** (Render + Streamlit Cloud)

## Endpoints da API

### `GET /weather/{cidade}`
Retorna dados climáticos atuais da cidade.

**Resposta:**
```json
{
  "city": "São Paulo",
  "country": "BR",
  "temperature": 23.5,
  "feels_like": 25.2,
  "humidity": 65,
  "wind_speed": 3.2,
  "description": "Céu Limpo",
  "icon": "01d"
}
```

### `GET /history/{cidade}`
Retorna histórico de consultas da cidade.

### `GET /forecast/{cidade}`
Retorna previsão de 5 dias da cidade.

**Resposta:**
```json
{
  "city": "São Paulo",
  "country": "BR",
  "forecasts": [
    {
      "datetime": "2024-01-15 12:00:00",
      "temperature": 25.3,
      "feels_like": 27.1,
      "humidity": 68,
      "wind_speed": 2.8,
      "description": "Parcialmente Nublado",
      "icon": "02d"
    }
  ]
}
```

### `GET /compare?cities=cidade1,cidade2,cidade3`
Compara múltiplas cidades (máximo 5).

### `GET /health`
Status da API.

## Instalação Local

### 1. Clone o repositório
```bash
git clone <seu-repo>
cd WeatherViz
```

### 2. Configure o ambiente
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Configure a API Key
```bash
cp .env.example .env
# Edite o .env e adicione sua chave do OpenWeatherMap
```

### 4. Execute a API
```bash
uvicorn main:app --reload
```
API disponível em: http://localhost:8000

### 5. Execute o Dashboard
```bash
streamlit run dashboard.py
```
Dashboard disponível em: http://localhost:8501

## Deploy

### 1. API (Render)
1. Acesse [Render](https://render.com) e conecte seu repositório
2. Crie um novo Web Service
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Adicione variável de ambiente: `OPENWEATHER_API_KEY`
5. Deploy! Anote a URL gerada

### 2. Dashboard (Streamlit Cloud)
1. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
2. Conecte seu repositório GitHub
3. Configure:
   - Main file: `dashboard.py`
   - Python version: 3.7+
4. Adicione secret: `API_BASE_URL` com a URL da sua API
5. Deploy!

### 3. Configuração Local para Produção
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edite secrets.toml com a URL real da sua API
```

## API Key OpenWeatherMap

1. Acesse [OpenWeatherMap](https://openweathermap.org/api)
2. Crie uma conta gratuita
3. Gere sua API Key
4. Configure no arquivo `.env`

## Tecnologias

- **Backend:** FastAPI, SQLite, Requests
- **Frontend:** Streamlit, Plotly, Pandas, NumPy
- **Deploy:** Render, Streamlit Cloud
- **API Externa:** OpenWeatherMap (Current Weather + 5 Day Forecast)

## Screenshots

*Em breve - adicionar GIFs de demonstração*

## Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

---

**WeatherViz** - Sistema profissional de consulta climática