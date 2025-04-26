from src.functions import *
from unittest.mock import patch

@patch('functions.requests.get')
def test_buscar_musica_real(mock_get):

    mock_response = {
        "data": [
            {
                "title": "Believer",
                "artist": {"name": "Imagine Dragons"},
                "album": {
                    "title": "Evolve",
                    "cover_medium": "https://link-da-capa.jpg"
                },
                "preview": "https://link-da-previa.mp3"
            }
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    resultado, erro = buscar_musica_deezer("Imagine Dragons")

    assert erro is None
    assert resultado["musica"] == "Believer"
    assert resultado["artista"] == "Imagine Dragons"
    assert resultado["album"] == "Evolve"

@patch('functions.requests.get')
def test_buscar_musica_erro(mock_get):

    mock_response = {"data": []}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    resultado, erro = buscar_musica_deezer("sadas1321658zxc")

    assert resultado is None
    assert erro == "Nenhuma música encontrada"

@patch('functions.requests.get')
def test_erro_na_api(mock_get):

    mock_get.return_value.status_code = 500

    resultado, erro = buscar_musica_deezer("Imagine Dragons")

    assert resultado is None
    assert erro == "Erro na API Deezer"