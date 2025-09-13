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
  },
  {
    "bairro": "Colonton",
    "cep": "93354",
    "cidade": "North Garyville",
    "data_aquisicao": "2021-11-30",
    "id": 2,
    "logradouro": "Price Prairie",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Travessa",
    "valor": 260070.0
  },
  {
    "bairro": "West Jennashire",
    "cep": "51116",
    "cidade": "Katherinefurt",
    "data_aquisicao": "2020-04-24",
    "id": 3,
    "logradouro": "Taylor Ranch",
    "tipo": "apartamento",
    "tipo_logradouro": "Avenida",
    "valor": 815970.0
  },
  {
    "bairro": "Reneeberg",
    "cep": "01631",
    "cidade": "Bentleymouth",
    "data_aquisicao": "2014-11-03",
    "id": 4,
    "logradouro": "Stacey Isle",
    "tipo": "terreno",
    "tipo_logradouro": "Avenida",
    "valor": 352507.0
  },
  {
    "bairro": "Burkeview",
    "cep": "09893",
    "cidade": "Port Cynthia",
    "data_aquisicao": "2023-05-10",
    "id": 5,
    "logradouro": "Taylor Causeway",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Rua",
    "valor": 929368.0
  }]
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis")

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
  },
  {
    "bairro": "Colonton",
    "cep": "93354",
    "cidade": "North Garyville",
    "data_aquisicao": "2021-11-30",
    "id": 2,
    "logradouro": "Price Prairie",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Travessa",
    "valor": 260070.0
  },
  {
    "bairro": "West Jennashire",
    "cep": "51116",
    "cidade": "Katherinefurt",
    "data_aquisicao": "2020-04-24",
    "id": 3,
    "logradouro": "Taylor Ranch",
    "tipo": "apartamento",
    "tipo_logradouro": "Avenida",
    "valor": 815970.0
  },
  {
    "bairro": "Reneeberg",
    "cep": "01631",
    "cidade": "Bentleymouth",
    "data_aquisicao": "2014-11-03",
    "id": 4,
    "logradouro": "Stacey Isle",
    "tipo": "terreno",
    "tipo_logradouro": "Avenida",
    "valor": 352507.0
  },
  {
    "bairro": "Burkeview",
    "cep": "09893",
    "cidade": "Port Cynthia",
    "data_aquisicao": "2023-05-10",
    "id": 5,
    "logradouro": "Taylor Causeway",
    "tipo": "casa em condominio",
    "tipo_logradouro": "Rua",
    "valor": 929368.0
  }]
    
    assert response.get_json() == esperado

@patch("api.connect_db")
def test_info_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [{
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
    response = client.get("/imoveis/1")

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
@patch("api.connect_db")
def test_criar_imovel(mock_connect_db, client):
  mock_conn = MagicMock()
  mock_cursor = MagicMock()
  mock_conn.cursor.return_value = mock_cursor
  mock_connect_db.return_value = mock_conn
  novo_imovel = {
        "bairro": "Vila Olimpia",
        "cep": "04546-042",
        "cidade": "São Paulo",
        "data_aquisicao": "2000-01-01",

        "logradouro": "Rua Quata",
        "tipo": "casa",
        "tipo_logradouro": "Rua",
        "valor": 500000.0
    
}
  response = client.post("/imoveis", json = novo_imovel)
  # Verifica resposta HTTP
  
  
  data = response.get_json()
  

  esperado = [{
        "bairro": "Vila Olimpia",
        "cep": "04546-042",
        "cidade": "São Paulo",
        "data_aquisicao": "2000-01-01",

        "logradouro": "Rua Quata",
        "tipo": "casa",
        "tipo_logradouro": "Rua",
        "valor": 500000.0
  }]
  
  assert response.status_code == 201
  assert data == esperado
  mock_cursor.execute.assert_called_once()
  mock_conn.commit.assert_called_once()