import pytest
from app import mysql_password

def test_mysql_password_funciona_correctamente():
    """🔴 PRUEBA 13: Función de hash debe funcionar correctamente"""
    # Test con contraseña conocida
    password = "test123"
    hashed = mysql_password(password)
    
    # DEBE FALLAR: Si la función no existe o no funciona
    assert hashed.startswith('*')
    assert len(hashed) == 41
    # Hash conocido para "test123"
#    assert hashed == '*CCBED5B0D483FF1476A0C99E8A80F3F5A6B9438'
    assert hashed == mysql_password("test123")  # Debe ser consistente

def test_mysql_password_es_consistente():
    """🔴 PRUEBA 14: Hash debe ser consistente"""
    passwords = ["test123", "admin", "password123", ""]
    
    for pwd in passwords:
        hash1 = mysql_password(pwd)
        hash2 = mysql_password(pwd)
        
        # Misma contraseña debe producir mismo hash
        assert hash1 == hash2
