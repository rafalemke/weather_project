from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherData(BaseModel):
    id: Optional[int] = None  # Opcional, pois pode ser gerado pelo banco de dados
    temperature: float
    pressure: float
    humidity: float
    timestamp: Optional[datetime] = None  # O banco pode definir automaticamente

class UserData(BaseModel):
    username: str
    password: str  # A senha deve ser tratada com hashing antes de ser salva no banco
    role: Optional[str] = "user"  # Papel do usuário no sistema
