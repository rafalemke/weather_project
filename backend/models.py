from pydantic import BaseModel

class WeatherData(BaseModel):
    temperature: float
    pressure: float
    humidity: float