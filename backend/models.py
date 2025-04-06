from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class WeatherData(BaseModel):
    temperature: float
    pressure: float
    humidity: float
    date: Optional[datetime] = None

class UserData(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"
    name: str

class WeatherQueryParams(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    limit: Optional[int] = 100
