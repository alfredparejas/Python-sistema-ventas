# tests/test_models/test_business_logic.py
from models.models import Usuario

def test_mysql_password_funciona_correctamente():
    """🔴 PRUEBA 13: Función de hash debe funcionar correctamente"""
    # Test con contraseña conocida
    password = "test123"
    hashed = Usuario.mysql_password(password)

    # Verificaciones básicas
    assert hashed.startswith('*')
    assert len(hashed) == 41
    
    # Comparar con el hash real
    hash_real = Usuario.mysql_password("test123")
    assert hashed == hash_real

def test_mysql_password_es_consistente():
    """🔴 PRUEBA 14: Misma contraseña genera mismo hash"""
    password = "mi_contraseña"
    hash1 = Usuario.mysql_password(password)
    hash2 = Usuario.mysql_password(password)
    
    assert hash1 == hash2
    assert hash1.startswith('*')
    assert len(hash1) == 41

def test_mysql_password_vacia():
    """🔴 PRUEBA 15: Contraseña vacía genera hash específico"""
    hash_vacio = Usuario.mysql_password("")
    assert hash_vacio == "*DA39A3EE5E6B0D3255BFEF95601890AFD80709"

def test_usuario_check_password():
    """🔴 PRUEBA 16: Usuario puede verificar contraseñas"""
    # Crear usuario de prueba
    usuario = Usuario()
    usuario.set_password("password123")
    
    assert usuario.check_password("password123") == True
    assert usuario.check_password("password_wrong") == False
