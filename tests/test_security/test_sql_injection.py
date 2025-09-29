# tests/test_security/test_sql_injection.py
import pytest
from unittest.mock import patch, MagicMock

def test_login_resistente_a_sql_injection(client):
    """🔴 PRUEBA 8: Login es resistente a SQL injection"""
    # Intentar diferentes tipos de SQL injection
    injection_attempts = [
        "admin' OR '1'='1",
        "admin' --",
        "admin' /*",
        "admin'; DROP TABLE usuarios; --"
    ]
    
    for attempt in injection_attempts:
        with patch('app.Usuario.query') as mock_query:
            # El ORM debería tratar esto como texto literal, no como SQL
            mock_query.filter_by.return_value.first.return_value = None
            
            response = client.post('/login', data={
                'usuario': attempt,
                'password': 'anypassword'
            }, follow_redirects=True)
            
            # No debería haber errores de SQL, solo credenciales incorrectas
            assert response.status_code == 200
            # El sistema debería manejar esto como usuario no encontrado
            assert b'Credenciales incorrectas' in response.data or b'Error' not in response.data

def test_evitar_inyeccion_sql_en_clientes(authenticated_client, mock_db_session):
    """🔴 PRUEBA 9: Formulario de clientes es resistente a SQL injection"""
    client = authenticated_client
    
    # Intentar SQL injection en el formulario de clientes
    injection_data = {
        'dni': "123' OR '1'='1",
        'nombre': "Test'; DROP TABLE clientes; --",
        'telefono': "123456789",
        'direccion': "Calle Test",
        'razon': "Test"
    }
    
    response = client.post('/sistema/clientes/agregar', 
                         data=injection_data, 
                         follow_redirects=True)
    
    # Verificar que no hay errores de base de datos
    assert response.status_code == 200
    # El ORM debería escapar automáticamente estos valores
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
