import pytest
from unittest.mock import patch
from mysql.connector import Error

def test_app_maneja_error_conexion_bd(client):
    """🔴 PRUEBA 9: App no debe caerse si BD no responde"""
    with patch('utils.db.get_connection', side_effect=Error("Connection failed")):
        response = client.get('/login')
        
        # La app debe seguir funcionando aunque BD falle
        assert response.status_code == 200
        # No debe mostrar errores técnicos
        assert b"traceback" not in response.data.lower()
        assert b"error" not in response.data.lower()  # No errores genéricos

def test_login_maneja_error_bd_gracefully(client):
    """🔴 PRUEBA 10: Login debe manejar errores de BD adecuadamente"""
    with patch('utils.db.get_connection', return_value=None):
        response = client.post('/login', data={
            'usuario': 'test@test.com',
            'password': 'test123'
        })
        
        # Cuando BD falla, debe mostrar mensaje adecuado
        assert response.status_code == 200
        # Puede mostrar "Credenciales incorrectas" o mensaje de error de conexión
        # Esto es un error real: debería distinguir entre error de BD y credenciales inválidas
        assert b'credenciales' in response.data.lower() or b'conexion' in response.data.lower()
