import psycopg2
from config import DATABASE

def get_connection():
    return psycopg2.connect(
        host=DATABASE["host"],
        database=DATABASE["database"],
        user=DATABASE["user"],
        password=DATABASE["password"]
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatura (
            id SERIAL PRIMARY KEY,
            valor FLOAT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

create_table()  # Garante que a tabela exista ao iniciar a API
