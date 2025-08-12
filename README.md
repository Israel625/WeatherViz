# 🌤️ WeatherViz

Sistema completo de consulta climática com API REST e dashboard interativo.

## 🚀 Funcionalidades

- **API REST** com FastAPI
- **Dashboard interativo** com Streamlit
- **Histórico de consultas** em SQLite
- **Gráficos dinâmicos** com Plotly
- **Deploy em nuvem** (Render + Streamlit Cloud)

## 📋 Endpoints da API

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

### `GET /health`
Status da API.

## 🛠️ Instalação Local

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

## 🌐 Deploy

### API (Render/Railway)
1. Conecte seu repositório
2. Configure a variável `OPENWEATHER_API_KEY`
3. Deploy automático

### Dashboard (Streamlit Cloud)
1. Conecte seu repositório no [Streamlit Cloud](https://streamlit.io/cloud)
2. Configure o arquivo principal: `dashboard.py`
3. Atualize a `API_BASE_URL` no dashboard

## 🔑 API Key OpenWeatherMap

1. Acesse [OpenWeatherMap](https://openweathermap.org/api)
2. Crie uma conta gratuita
3. Gere sua API Key
4. Configure no arquivo `.env`

## 📊 Tecnologias

- **Backend:** FastAPI, SQLite, Requests
- **Frontend:** Streamlit, Plotly, Pandas
- **Deploy:** Render, Streamlit Cloud
- **API Externa:** OpenWeatherMap

## 📸 Screenshots

*Em breve - adicionar GIFs de demonstração*

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**WeatherViz** - Sistema profissional de consulta climática 🌤️