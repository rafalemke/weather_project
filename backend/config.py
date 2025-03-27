import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa realmente se conectar
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

DATABASE = {
    "host": "localhost",
    "database": "itacarnijo",
    "user": "teste",
    "password": "1234"
}

API_HOST = get_local_ip()
API_PORT = 8000
