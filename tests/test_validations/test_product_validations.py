# tests/test_validations/test_product_validations.py
import pytest

def test_producto_no_acepta_codigo_vacio(authenticated_client):
    """🔴 PRUEBA 12: Producto valida código no vacío"""
    client = authenticated_client
    
    response = client.post('/sistema/productos/agregar', data={
        'codigo': '',  # código vacío
        'descripcion': 'Producto test',
        'cantidad': '10',
        'precio': '100',
        'proveedor': '1'
    }, follow_redirects=True)
    
    assert b'El c\xc3\xb3digo del producto es requerido' in response.data

def test_producto_no_acepta_precio_negativo(authenticated_client):
    """🔴 PRUEBA 13: Producto valida precio no negativo"""
    client = authenticated_client
    
    response = client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST001',
        'descripcion': 'Producto test',
        'cantidad': '10',
        'precio': '-100',  # precio negativo
        'proveedor': '1'
    }, follow_redirects=True)
    
    assert b'El precio no puede ser negativo' in response.data

def test_producto_no_acepta_stock_negativo(authenticated_client):
    """🔴 PRUEBA 14: Producto valida stock no negativo"""
    client = authenticated_client
    
    response = client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST001',
        'descripcion': 'Producto test',
        'cantidad': '-5',  # stock negativo
        'precio': '100',
        'proveedor': '1'
    }, follow_redirects=True)
    
    assert b'La cantidad no puede ser negativa' in response.data

def test_producto_valida_precio_numerico(authenticated_client):
    """🔴 PRUEBA 15: Producto valida que precio sea numérico"""
    client = authenticated_client
    
    response = client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST001',
        'descripcion': 'Producto test',
        'cantidad': '10',
        'precio': 'precio_invalido',  # precio no numérico
        'proveedor': '1'
    }, follow_redirects=True)
    
    assert b'El precio debe ser un n\xc3\xbamero v\xc3\xa1lido' in response.data

def test_producto_valida_descripcion_no_vacia(authenticated_client):
    """🔴 PRUEBA 16: Producto valida descripción no vacía"""
    client = authenticated_client
    
    response = client.post('/sistema/productos/agregar', data={
        'codigo': 'TEST001',
        'descripcion': '',  # descripción vacía
        'cantidad': '10',
        'precio': '100',
        'proveedor': '1'
    }, follow_redirects=True)
    
    assert b'La descripci\xc3\xb3n del producto es requerida' in response.data
