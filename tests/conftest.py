import pytest
import sys
import os
from unittest.mock import Mock, patch

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def client():
    """Fixture para cliente de pruebas Flask"""
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_client(client):
    """Cliente con sesión autenticada"""
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['user_name'] = 'Test User'
    return client

@pytest.fixture
def mock_db():
    """Mock de la base de datos"""
    with patch('utils.db.get_connection') as mock:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock.return_value = mock_conn
        yield mock_conn, mock_cursor
