from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI(title="Buscador de Músicas Deezer")

#função para busca de músicas
@app.get("/buscar")
def buscar_musica(q: str):
    url = f"https://api.deezer.com/search?q={q}"
    resposta = requests.get(url)