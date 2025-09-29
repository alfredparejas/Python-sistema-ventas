# tests/test_validations/test_cliente_validations.py
import pytest

def test_cliente_valida_dni_no_vacio(authenticated_client, mock_db_session):
    """🔴 PRUEBA 10: Cliente valida DNI no vacío"""
    client = authenticated_client
    
    response = client.post('/sistema/clientes/agregar', data={
        'dni': '',  # DNI vacío
        'nombre': 'Cliente Test',
        'telefono': '123456789',
        'direccion': 'Calle Test',
        'razon': 'Test'
    }, follow_redirects=True)
    
    # Verificar que se muestra mensaje de error
    assert b'El DNI del cliente es requerido' in response.data
    # Verificar que NO se llamó a commit (no se guardó)
    mock_db_session.commit.assert_not_called()

def test_cliente_valida_nombre_no_vacio(authenticated_client, mock_db_session):
    """🔴 PRUEBA 11: Cliente valida nombre no vacío"""
    client = authenticated_client
    
    response = client.post('/sistema/clientes/agregar', data={
        'dni': '12345678',
        'nombre': '',  # Nombre vacío
        'telefono': '123456789',
        'direccion': 'Calle Test',
        'razon': 'Test'
    }, follow_redirects=True)
    
    # Verificar que se muestra mensaje de error
    assert b'El nombre del cliente es requerido' in response.data
    # Verificar que NO se llamó a commit (no se guardó)
    mock_db_session.commit.assert_not_called()
