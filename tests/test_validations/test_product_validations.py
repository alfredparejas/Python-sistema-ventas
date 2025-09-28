import pytest

def test_producto_no_acepta_codigo_vacio(auth_client, mock_db):
    """🔴 PRUEBA 3: Producto no debe aceptar código vacío"""
    mock_conn, mock_cursor = mock_db
    
    response = auth_client.post('/sistema/productos/agregar', data={
        'codigo': '',  # VACÍO - debería fallar
        'descripcion': 'Producto Test',
        'cantidad': '10',
        'precio': '100',
        'proveedor': '1'
    }, follow_redirects=True)
    
    # CORREGIDO: Usar solo ASCII en cadenas bytes
    assert b'codigo' in response.data.lower() or b'requerido' in response.data.lower()
    # No debe llamar a la base de datos si la validación falla
    assert not mock_cursor.execute.called

def test_producto_no_acepta_precio_negativo(auth_client, mock_db):
    """🔴 PRUEBA 4: No debe aceptar precios negativos"""
    mock_conn, mock_cursor = mock_db
    
    response = auth_client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST123',
        'descripcion': 'Producto Test',
        'cantidad': '10',
        'precio': '-100',  # NEGATIVO - debería fallar
        'proveedor': '1'
    }, follow_redirects=True)
    
    # CORREGIDO: Usar solo ASCII
    assert b'precio' in response.data.lower() and b'negativo' in response.data.lower()
    assert not mock_cursor.execute.called

def test_producto_no_acepta_stock_negativo(auth_client, mock_db):
    """🔴 PRUEBA 5: Stock no puede ser negativo"""
    mock_conn, mock_cursor = mock_db
    
    response = auth_client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST123',
        'descripcion': 'Producto Test', 
        'cantidad': '-5',  # NEGATIVO - debería fallar
        'precio': '100',
        'proveedor': '1'
    }, follow_redirects=True)
    
    # CORREGIDO: Usar solo ASCII
    assert b'cantidad' in response.data.lower() and b'negativo' in response.data.lower()
    assert not mock_cursor.execute.called

def test_producto_valida_precio_numerico(auth_client, mock_db):
    """🔴 PRUEBA 6: Precio debe ser numérico"""
    mock_conn, mock_cursor = mock_db
    
    response = auth_client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST123',
        'descripcion': 'Producto Test',
        'cantidad': '10',
        'precio': 'precio_invalido',  # TEXTO - debería fallar
        'proveedor': '1'
    }, follow_redirects=True)
    
    # CORREGIDO: Usar solo ASCII
    assert b'numero' in response.data.lower() or b'valido' in response.data.lower()
