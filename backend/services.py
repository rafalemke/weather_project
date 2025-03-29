from .database import get_connection
from .security import verify_password, hash_password


def insert_user(username: str, password: str, role: str = "user"):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)  # Gera o hash da senha
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, hashed_password, role)
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


def get_weather_data(limit=100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Retorna os resultados como dicionários
    cursor.execute("SELECT * FROM weather_data ORDER BY date DESC LIMIT %s", (limit,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records