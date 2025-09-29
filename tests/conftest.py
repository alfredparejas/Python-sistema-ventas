# tests/conftest.py
import os
import sys
import pytest

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from models.models import db
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    """Fixture para la aplicación Flask"""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Deshabilitar CSRF para tests
    
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    """Fixture para el cliente de测试"""
    return app.test_client()

@pytest.fixture
def mock_db_session():
    """Mock de la sesión de base de datos para ORM"""
    with patch('app.db.session') as mock_session:
        mock_commit = MagicMock()
        mock_session.commit = mock_commit
        mock_add = MagicMock()
        mock_session.add = mock_add
        mock_session.rollback = MagicMock()
        yield mock_session

@pytest.fixture
def mock_usuario():
    """Mock de usuario para tests de autenticación"""
    with patch('app.Usuario.query') as mock_query:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.nombre = "Test User"
        mock_user.correo = "test@example.com"
        mock_user.check_password.return_value = True
        mock_query.filter_by.return_value.first.return_value = mock_user
        yield mock_query

@pytest.fixture
def authenticated_client(client):
    """Cliente con sesión autenticada"""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_name'] = 'Test User'
    return client
