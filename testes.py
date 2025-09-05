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
    
    mock_cursor.fetchall.return_value = []
    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis")

    assert response.status_code == 404