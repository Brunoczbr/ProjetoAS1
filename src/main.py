from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from functions import get_html_homepage, buscar_musica_deezer

app = FastAPI(title="Buscador de Músicas Deezer")
@app.get("/", response_class=HTMLResponse)
def homepage():
    return get_html_homepage()

@app.get("/buscar")
def buscar_musica(q: str):

    resultado, erro = buscar_musica_deezer(q)

    if erro == "Erro na API Deezer":
        return JSONResponse(status_code=500, content={"erro": "Não foi possível acessar a API do Deezer, tente novamente."})

    elif erro == "Nenhuma música encontrada":
        return JSONResponse(status_code=404, content={"mensagem": "Nenhuma música encontrada."})

    return resultado