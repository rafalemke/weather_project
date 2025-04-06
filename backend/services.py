from .database import get_connection
from .security import hash_password
from typing import Optional
from datetime import date

def insert_user(name: str, username: str, password: str, role: str = "user"):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)",
        (name, username, hashed_password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

def insert_weather_data(temperature: float, pressure: float, humidity: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather_data (temperature, pressure, humidity) VALUES (%s, %s, %s)",
        (temperature, pressure, humidity)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_weather_data(start_date: Optional[date] = None, end_date: Optional[date] = None, limit=100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM weather_data"
    conditions = []
    params = []

    if start_date:
        conditions.append("DATE(date) >= %s")
        params.append(start_date)

    if end_date:
        conditions.append("DATE(date) <= %s")
        params.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY date DESC LIMIT %s"
    params.append(limit)

    cursor.execute(query, params)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records
