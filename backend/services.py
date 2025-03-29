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

def authenticate_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and verify_password(password, user[0]):  # Verifica o hash da senha
        return {"username": username, "role": user[1]}
    return None

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

def get_weather_data(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data ORDER BY date DESC LIMIT %s", (limit,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"date": record[0], "temperature": record[1], "pressure": record[2], "humidity": record[3]} for record in records]

def get_weather_data(limit=100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Retorna os resultados como dicionários
    cursor.execute("SELECT * FROM weather_data ORDER BY date DESC LIMIT %s", (limit,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records