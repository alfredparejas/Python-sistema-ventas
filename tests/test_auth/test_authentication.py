# tests/test_auth/test_authentication.py
import pytest
from unittest.mock import patch, MagicMock

def test_endpoints_criticos_requieren_autenticacion(client):
    """🔴 PRUEBA 1: Endpoints críticos redirigen a login sin autenticación"""
    # Probar varios endpoints sin sesión
    endpoints = [
        '/sistema',
        '/sistema/nueva_venta', 
        '/sistema/clientes',
        '/sistema/proveedores',
        '/sistema/productos',
        '/sistema/ventas',
        '/sistema/reportes'
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint, follow_redirects=False)
        assert response.status_code in [302, 401]  # Redirección o no autorizado
        if response.status_code == 302:
            assert '/login' in response.location

def test_logout_limpia_sesion_correctamente(authenticated_client):
    """🔴 PRUEBA 2: Logout limpia la sesión correctamente"""
    client = authenticated_client
    
    # Verificar que hay sesión antes del logout
    with client.session_transaction() as sess:
        assert 'user_id' in sess
    
    # Hacer logout
    response = client.get('/logout', follow_redirects=True)
    
    # Verificar redirección a login
    assert response.status_code == 200
    assert b'login' in response.data.lower()
    
    # Verificar que la sesión fue limpiada
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'user_name' not in sess

def test_login_con_credenciales_validas(client, mock_usuario):
    """🔴 PRUEBA 3: Login funciona con credenciales válidas"""
    # Intentar login
    response = client.post('/login', data={
        'usuario': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    # Verificar redirección al sistema
    assert response.status_code == 200
    # Verificar que se estableció la sesión
    with client.session_transaction() as sess:
        assert sess['user_id'] == 1
        assert sess['user_name'] == "Test User"

def test_login_con_credenciales_invalidas(client):
    """🔴 PRUEBA 4: Login falla con credenciales inválidas"""
    with patch('app.Usuario.query') as mock_query:
        # Mock usuario que no existe
        mock_query.filter_by.return_value.first.return_value = None
        
        response = client.post('/login', data={
            'usuario': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Credenciales incorrectas' in response.data

def test_login_con_campos_vacios(client):
    """🔴 PRUEBA 5: Login valida campos vacíos"""
    # Test con usuario vacío
    response = client.post('/login', data={
        'usuario': '',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert b'Completa todos los campos' in response.data
    
    # Test con password vacío
    response = client.post('/login', data={
        'usuario': 'test@example.com',
        'password': ''
    }, follow_redirects=True)
    
    assert b'Completa todos los campos' in response.data
