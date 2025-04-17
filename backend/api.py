import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import date
from backend.models import WeatherData
from backend.services import get_weather_data, insert_weather_data, get_extremos
from backend.config import API_HOST, API_PORT

app = FastAPI()

# Permitir requisições do frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar para domínio específico em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register_data(data: WeatherData):
    insert_weather_data(data.temperature, data.pressure, data.humidity)
    return {"status": "ok", "data": data}

@app.get("/data")
def list_data(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(100)
):
    """
    Retorna os dados meteorológicos com filtros opcionais por data e limite.
    """
    data = get_weather_data(start_date=start_date, end_date=end_date, limit=limit)
    return {"data": data}

@app.get("/extremos")
def extremos():
    """
    Retorna os valores máximos e mínimos de temperatura, umidade e pressão, e as datas desses registros.
    """
    data = get_extremos()
    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
