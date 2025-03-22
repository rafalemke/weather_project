import mysql.connector
from config import DATABASE

def get_connection():
    return mysql.connector.connect(
        host=DATABASE["host"],
        database=DATABASE["database"],
        user=DATABASE["user"],
        password=DATABASE["password"]
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS esp32_sensor (
            id SERIAL PRIMARY KEY,
            distance FLOAT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

create_table()  # Garante que a tabela exista ao iniciar a API
