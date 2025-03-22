from fastapi import FastAPI
from models import Distance
from services import inserir_medida, obter_medidas
from config import API_HOST, API_PORT

app = FastAPI()

@app.post("/registrar")
def registrar_medida(dado: Distance):
    inserir_medida(dado.distance)
    return {"status": "ok", "distance": dado.distance}

@app.get("/dados")
def listar_dados():
    return {"dados": obter_medidas()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
