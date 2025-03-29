import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import WeatherData
from backend.services import get_weather_data, insert_weather_data
from backend.config import API_HOST, API_PORT


app = FastAPI()

# Permitir requisições do frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir para um domínio específico depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register_data(data: WeatherData):
    insert_weather_data(data.temperature, data.pressure, data.humidity)
    return {"status": "ok", "data": data}

@app.get("/data")
def list_data():
    return {"data": get_weather_data()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)