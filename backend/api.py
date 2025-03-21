from fastapi import FastAPI
from models import Temperatura
from services import inserir_temperatura, obter_temperaturas
from config import API_HOST, API_PORT

app = FastAPI()

@app.post("/registrar")
def registrar_temp(dado: Temperatura):
    inserir_temperatura(dado.valor)
    return {"status": "ok", "temperatura": dado.valor}

@app.get("/dados")
def listar_dados():
    return {"dados": obter_temperaturas()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
