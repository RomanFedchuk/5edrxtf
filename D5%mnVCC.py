import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        datetime TEXT,
        temperature REAL
    )
''')
conn.commit()

url = 'https://www.weather.com/weather/today/l/UPXX0014:1:UA'  # Актуальний URL для Житомира

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

temperature_tag = soup.find('span', class_='CurrentConditions--tempValue--3KcTQ')  # Замініть на актуальний тег та клас
temperature = temperature_tag.text if temperature_tag else None

if temperature:

    temperature = float(temperature.replace('°', '').replace('C', '').strip())

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO weather_data (datetime, temperature)
        VALUES (?, ?)
    ''', (current_datetime, temperature))
    conn.commit()
    print(f"Дані успішно додані: {current_datetime}, {temperature}°C")
else:
    print("Не вдалося отримати температуру з веб-сайту.")

conn.close()