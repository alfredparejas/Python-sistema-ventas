import pytest

def test_login_resistente_a_sql_injection(client):
    """🔴 PRUEBA 1: Login debe resistir inyección SQL"""
    # Intentar inyecciones SQL comunes
    payloads = [
        "admin' OR '1'='1",
        "admin' --",
        "admin' #", 
        "admin' /*",
        "' OR 1=1--"
    ]
    
    for payload in payloads:
        response = client.post('/login', data={
            'usuario': payload,
            'password': 'anypassword'
        })
        
        # No debe haber errores de SQL en la respuesta
        assert response.status_code in [200, 302]
        assert b"sql" not in response.data.lower()
        assert b"syntax" not in response.data.lower()
        assert b"mysql" not in response.data.lower()

def test_evitar_inyeccion_sql_en_clientes(auth_client, mock_db):
    """🔴 PRUEBA 2: Evitar inyección SQL en búsqueda de clientes"""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = []
    
    # Intentar inyección en parámetro de búsqueda
    response = auth_client.get('/sistema/clientes?search=test\' OR 1=1--')
    
    assert response.status_code == 200
    # Verificar que no se ejecuta SQL peligroso
    assert not any("OR 1=1" in str(call) for call in mock_cursor.execute.call_args_list)
