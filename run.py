#!/usr/bin/env python3
"""
Script para executar o WeatherViz em modo desenvolvimento
"""
import subprocess
import sys
import os
from threading import Thread
import time

def run_api():
    """Executa a API FastAPI"""
    print("🚀 Iniciando API FastAPI...")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

def run_dashboard():
    """Executa o dashboard Streamlit"""
    print("📊 Iniciando Dashboard Streamlit...")
    time.sleep(3)  # Aguarda API iniciar
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", "8501"])

def main():
    print("🌤️ WeatherViz - Iniciando aplicação completa...")
    print("=" * 50)
    
    # Verifica se o arquivo .env existe
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado!")
        print("📝 Copie o .env.example e configure sua API key do OpenWeatherMap")
        return
    
    try:
        # Inicia API em thread separada
        api_thread = Thread(target=run_api, daemon=True)
        api_thread.start()
        
        # Inicia Dashboard
        run_dashboard()
        
    except KeyboardInterrupt:
        print("\n👋 Encerrando WeatherViz...")
        sys.exit(0)

if __name__ == "__main__":
    main()