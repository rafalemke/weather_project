import bcrypt
from backend.database import get_connection
from mysql.connector import Error

# Gerar um hash seguro para a senha
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

# Verificar uma senha fornecida com o hash armazenado
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# Autenticar usuário no banco de dados
def authenticate_user(username: str, password: str):
    conn = None
    user = None

    try:
        conn = get_connection()
        if conn is None:
            print("❌ Erro: Falha ao conectar ao banco de dados.")
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT name, password, role FROM users WHERE username = %s LIMIT 1", (username,))
        user = cursor.fetchone()
        
    except Error as e:
        print(f"❌ Erro ao buscar usuário: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if user and verify_password(password, user[1]):  # Verifica o hash da senha
        return {"username": username, "role": user[2], "name": user[0]}
    
    return None
