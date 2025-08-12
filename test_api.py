#!/usr/bin/env python3
"""
Script de teste para validar a API WeatherViz
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"

def test_health():
    """Testa endpoint de health"""
    print("🔍 Testando /health...")
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_weather(city="São Paulo"):
    """Testa endpoint de clima"""
    print(f"🌤️ Testando /weather/{city}...")
    try:
        response = requests.get(f"{API_BASE}/weather/{city}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Cidade: {data['city']}")
            print(f"Temperatura: {data['temperature']}°C")
            print(f"Descrição: {data['description']}")
            return True
        else:
            print(f"Erro: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_history(city="São Paulo"):
    """Testa endpoint de histórico"""
    print(f"📊 Testando /history/{city}...")
    try:
        response = requests.get(f"{API_BASE}/history/{city}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Registros encontrados: {len(data)}")
            return True
        else:
            print(f"Erro: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🧪 WeatherViz - Testes da API")
    print("=" * 40)
    
    # Verifica se API está rodando
    try:
        requests.get(API_BASE, timeout=5)
    except:
        print("❌ API não está rodando!")
        print("💡 Execute: uvicorn main:app --reload")
        return
    
    # Verifica API key
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("⚠️  OPENWEATHER_API_KEY não configurada!")
        return
    
    # Executa testes
    tests = [
        ("Health Check", test_health),
        ("Weather Data", lambda: test_weather("São Paulo")),
        ("History Data", lambda: test_history("São Paulo"))
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*20}")
        result = test_func()
        results.append((name, result))
        print("✅ PASSOU" if result else "❌ FALHOU")
    
    # Resumo
    print(f"\n{'='*40}")
    print("📋 RESUMO DOS TESTES:")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, result in results if result)
    print(f"\n🎯 {passed}/{len(results)} testes passaram")

if __name__ == "__main__":
    main()