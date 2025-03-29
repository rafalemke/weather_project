import requests
from backend.config import API_HOST, API_PORT

API_URL = f"http://{API_HOST}:{API_PORT}"

def fetch_data_from_api():
    """Busca os dados meteorológicos da API FastAPI"""
    try:
        response = requests.get(f"{API_URL}/data")
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

