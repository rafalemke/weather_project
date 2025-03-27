import mysql.connector
from .config import DATABASE

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

    # Criação da tabela weather_data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,       
            temperature VARCHAR(50),
            pressure VARCHAR(50),
            humidity VARCHAR(50)
            
        );
    """)

    # Criação da tabela users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user'
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

create_table()  # Garante que a tabela exista ao iniciar a API
