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

    if resposta.status_code != 200:
        return JSONResponse(status_code=500, content={"erro": "Não foi possível acessar a API do Deezer, tente novamente."})

    dados = resposta.json()
    if not dados["data"]:
        return JSONResponse(status_code=404, content={"mensagem": "Nenhuma música encontrada."})

    