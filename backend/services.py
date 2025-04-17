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


def get_extremos():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            MAX(temperature), MIN(temperature),
            MAX(humidity), MIN(humidity),
            MAX(pressure), MIN(pressure)
        FROM weather_data
    """
    cursor.execute(query)
    result = cursor.fetchone()

    # Datas dos extremos
    query_dates = """
        SELECT 
            (SELECT date FROM weather_data ORDER BY temperature DESC LIMIT 1),
            (SELECT date FROM weather_data ORDER BY temperature ASC LIMIT 1),
            (SELECT date FROM weather_data ORDER BY humidity DESC LIMIT 1),
            (SELECT date FROM weather_data ORDER BY humidity ASC LIMIT 1),
            (SELECT date FROM weather_data ORDER BY pressure DESC LIMIT 1),
            (SELECT date FROM weather_data ORDER BY pressure ASC LIMIT 1)
    """
    cursor.execute(query_dates)
    dates = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "max_temp": result[0], "min_temp": result[1],
        "max_humidity": result[2], "min_humidity": result[3],
        "max_pressure": result[4], "min_pressure": result[5],
        "dates": {
            "temp_max": dates[0], "temp_min": dates[1],
            "hum_max": dates[2], "hum_min": dates[3],
            "press_max": dates[4], "press_min": dates[5],
        }
    }


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
