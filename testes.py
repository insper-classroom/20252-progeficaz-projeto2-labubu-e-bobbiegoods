import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db


@pytest.fixture
def client():
   
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
@patch("api.connect_db")
def test_get_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [{
    "bairro": "Lake Danielle",
    "cep": "85184",
    "cidade": "Judymouth",
    "data_aquisicao": "2017-07-29",
    "id": 1,
    "logradouro": "Nicole Common",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Travessa",
    "valor": 488424.0
  }]
    mock_connect_db.return_value = mock_conn
    response = client.get("/")

    esperado = [{
    "bairro": "Lake Danielle",
    "cep": "85184",
    "cidade": "Judymouth",
    "data_aquisicao": "2017-07-29",
    "id": 1,
    "logradouro": "Nicole Common",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Travessa",
    "valor": 488424.0
  }]
    
    assert response.get_json() == esperado