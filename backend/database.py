import mysql.connector
from mysql.connector import Error
from backend.config import DATABASE

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    try:
        conn = mysql.connector.connect(
            host=DATABASE["host"],
            database=DATABASE["database"],
            user=DATABASE["user"],
            password=DATABASE["password"]
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def create_table():
    """Cria as tabelas caso não existam no banco de dados."""
    conn = get_connection()
    if conn is None:
        print("❌ Falha na conexão com o banco de dados.")
        return
    
    try:
        cursor = conn.cursor()

        # Criação da tabela weather_data com tipos corretos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperature FLOAT NOT NULL,
                pressure FLOAT NOT NULL,
                humidity FLOAT NOT NULL
            );
        """)

        # Criação da tabela users com hash de senha
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('user', 'admin') DEFAULT 'user'
            );
        """)

        conn.commit()
        print("✅ Tabelas verificadas/criadas com sucesso.")

    except Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

# Se desejar criar as tabelas automaticamente ao rodar o código:
if __name__ == "__main__":
    create_table()
