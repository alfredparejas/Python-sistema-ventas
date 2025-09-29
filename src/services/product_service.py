from utils.db import get_connection

class ProductoService:
    """Servicio para operaciones con productos"""
    
    @staticmethod
    def crear_producto(codigo, descripcion, cantidad, precio, id_proveedor):
        """Crea un nuevo producto en la base de datos"""
        conn = get_connection()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO productos (codigo, descripcion, cantidad, precio, id_proveedor) VALUES (%s, %s, %s, %s, %s)",
                (codigo, descripcion, cantidad, precio, id_proveedor)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
