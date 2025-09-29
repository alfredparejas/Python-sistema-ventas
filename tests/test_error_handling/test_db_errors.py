# tests/test_error_handling/test_db_errors.py
import pytest
from unittest.mock import patch, MagicMock

def test_app_maneja_error_conexion_bd(client):
    """🔴 PRUEBA 6: App maneja errores de conexión a BD"""
    with patch('app.Usuario.query') as mock_query:
        # Simular error de base de datos
        mock_query.filter_by.side_effect = Exception("Error de conexión")
        
        response = client.post('/login', data={
            'usuario': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Verificar que se muestra mensaje de error
        assert b'Error de conexi' in response.data

def test_login_maneja_error_bd_gracefully(client):
    """🔴 PRUEBA 7: Login maneja errores de BD gracefulmente"""
    with patch('app.Usuario.query') as mock_query:
        # Simular diferentes errores de BD
        errors = [
            Exception("Connection refused"),
            Exception("Database timeout"),
            Exception("Query failed")
        ]
        
        for error in errors:
            mock_query.filter_by.side_effect = error
            
            response = client.post('/login', data={
                'usuario': 'test@example.com',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Verificar que no hay crash y se muestra error
            assert response.status_code == 200
            assert b'Error' in response.data
