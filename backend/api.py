from fastapi import FastAPI
from backend.models import WeatherData
from backend.services import get_weather_data, insert_weather_data
from backend.config import API_HOST, API_PORT


app = FastAPI()

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