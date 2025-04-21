from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI(title="Buscador de Músicas Deezer")
@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
    <html>
    <head>
        <title>Buscar Música</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; }
            input { padding: 10px; width: 80%; margin-right: 10px; }
            button { padding: 10px; }
            img { max-width: 100%; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Buscar Música no Deezer</h1>
        <input id="busca" placeholder="Digite o nome da música ou artista" />
        <button onclick="buscar()">Buscar</button>
        <div id="resultado" style="margin-top:20px;"></div>

        <script>
            async function buscar() {
                const termo = document.getElementById('busca').value;
                const resposta = await fetch('/buscar?q=' + encodeURIComponent(termo));
                const resultadoDiv = document.getElementById('resultado');
                if (resposta.ok) {
                    const data = await resposta.json();
                    resultadoDiv.innerHTML = `
                        <h3>${data.musica} - ${data.artista}</h3>
                        <p><strong>Álbum:</strong> ${data.album}</p>
                        <img src="${data.capa}" alt="Capa do álbum">
                        <p><audio controls src="${data.previa}"></audio></p>
                    `;
                } else {
                    resultadoDiv.innerHTML = "<p>🎧 Nenhuma música encontrada.</p>";
                }
            }
        </script>
    </body>
    </html>
    """

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

    primeira = dados["data"][0]
    resultado = {
        "musica": primeira["title"],
        "artista": primeira["artist"]["name"],
        "album": primeira["album"]["title"],
        "capa": primeira["album"]["cover_medium"],
        "previa": primeira["preview"]
    }
    return resultado