import sqlite3
from datetime import datetime
from typing import List, Dict

class WeatherDB:
    def __init__(self, db_path: str = "weather.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity INTEGER NOT NULL,
                    wind_speed REAL NOT NULL,
                    feels_like REAL NOT NULL,
                    description TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def save_weather_data(self, city: str, weather_data: Dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO weather_history 
                (city, temperature, humidity, wind_speed, feels_like, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                city.lower(),
                weather_data['temperature'],
                weather_data['humidity'],
                weather_data['wind_speed'],
                weather_data['feels_like'],
                weather_data['description']
            ))
    
    def get_city_history(self, city: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM weather_history 
                WHERE city = ? 
                ORDER BY timestamp DESC 
                LIMIT 50
            """, (city.lower(),))
            return [dict(row) for row in cursor.fetchall()]