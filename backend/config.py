import socket
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

def get_local_ip():
    """Obtém o IP local da máquina."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Configuração do Banco de Dados
DATABASE = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "itacarnijo"),
    "user": os.getenv("DB_USER", "teste"),
    "password": os.getenv("DB_PASSWORD", "1234")
}

# Configuração da API
API_HOST = os.getenv("API_HOST", get_local_ip())
if API_HOST == "0.0.0.0":  # Se for 0.0.0.0, substitui pelo IP local
    API_HOST = get_local_ip()

API_PORT = int(os.getenv("API_PORT", 8000))  # Porta padrão 8000

print(API_HOST,API_PORT)