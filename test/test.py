from src.functions import *
from unittest.mock import patch


@patch('src.functions.requests.get')
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

@patch('src.functions.requests.get')
def test_buscar_musica_erro(mock_get):
        mock_response = {"data": []}

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        resultado, erro = buscar_musica_deezer("sadas1321658zxc")

        assert resultado is None
        assert erro == "Nenhuma música encontrada"

@patch('src.functions.requests.get')
def test_erro_na_api(mock_get):

    mock_get.return_value.status_code = 500

    resultado, erro = buscar_musica_deezer("Imagine Dragons")

    assert resultado is None
    assert erro == "Erro na API Deezer"

@patch('src.functions.requests.get')
def test_busca_vazia(mock_get):
    with patch('src.functions.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": []}

        resultado, erro = buscar_musica_deezer("")

        assert resultado is None
        assert erro == "Nenhuma música encontrada"

@patch('src.functions.requests.get')
def test_timeout_na_api(mock_get):
    # Simula que a requisição levanta um Timeout
    mock_get.side_effect = requests.exceptions.Timeout

    resultado, erro = buscar_musica_deezer("Imagine Dragons")

    assert resultado is None
    assert erro == "Timeout ao tentar acessar a API Deezer"