# Importa la nueva librería para SQL Server
import pyodbc

class DataBase:
    def __init__(self):
        # --- IMPORTANTE: MODIFICA ESTA LÍNEA CON EL NOMBRE DE TU SERVIDOR ---
        self.server_name = 'GIt_ConstrucciónSoftware'
        self.database_name = 'MiniMarketDB'
        self.connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server_name};'
            f'DATABASE={self.database_name};'
            f'Trusted_Connection=yes;'
        )
        self.con = None
        self.cur = None

    def conectar(self):
        """Establece la conexión con la base de datos SQL Server."""
        try:
            self.con = pyodbc.connect(self.connection_string)
            self.cur = self.con.cursor()
            return True
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error de conexión a la base de datos: {sqlstate}")
            return False

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.con:
            self.con.close()

    # ==================================================
    # MÉTODOS PARA PRODUCTOS
    # ==================================================
    def ver_productos(self):
        if not self.conectar():
            return []
        try:
            # Seleccionamos las columnas que necesitamos para la tabla de la UI
            sql = "SELECT ProductoID, SKU, Nombre, Precio, Stock FROM Producto"
            self.cur.execute(sql)
            productos = self.cur.fetchall()
            return productos
        except pyodbc.Error as e:
            print(f"Error al ver productos: {e}")
            return []
        finally:
            self.desconectar()

    def registrar_producto(self, sku, nombre, precio, stock):
        if not self.conectar():
            return False
        try:
            sql = "INSERT INTO Producto (SKU, Nombre, Precio, Stock) VALUES (?, ?, ?, ?)"
            self.cur.execute(sql, sku, nombre, precio, stock)
            self.con.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error al registrar producto: {e}")
            return False
        finally:
            self.desconectar()

    def eliminar_producto(self, producto_id):
        if not self.conectar():
            return False
        try:
            sql = "DELETE FROM Producto WHERE ProductoID = ?"
            self.cur.execute(sql, producto_id)
            self.con.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            self.desconectar()
    
    def actualizar_producto(self, producto_id, sku, nombre, precio, stock):
        if not self.conectar():
            return False
        try:
            sql = """
                UPDATE Producto 
                SET SKU = ?, Nombre = ?, Precio = ?, Stock = ? 
                WHERE ProductoID = ?
            """
            self.cur.execute(sql, sku, nombre, precio, stock, producto_id)
            self.con.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            self.desconectar()

    # ==================================================
    # MÉTODOS PARA CLIENTES (Adaptado a la nueva tabla Cliente)
    # ==================================================
    def ver_clientes(self):
        if not self.conectar():
            return []
        try:
            sql = "SELECT ClienteID, NombreCompleto, DocumentoIdentidad, Telefono, Email FROM Cliente"
            self.cur.execute(sql)
            clientes = self.cur.fetchall()
            return clientes
        except pyodbc.Error as e:
            print(f"Error al ver clientes: {e}")
            return []
        finally:
            self.desconectar()

  
    # ==================================================
    # MÉTODOS PARA VENTAS (Nuevas funciones)
    # ==================================================
    def registrar_venta(self, cliente_id, total):
        """Registra la cabecera de la venta y devuelve el ID de la nueva venta."""
        if not self.conectar():
            return None
        try:
            # Usamos SCOPE_IDENTITY() para obtener el ID recién creado
            sql = """
                INSERT INTO Venta (ClienteID, Total) 
                OUTPUT INSERTED.VentaID 
                VALUES (?, ?)
            """
            # El ClienteID puede ser None si es una venta genérica
            self.cur.execute(sql, cliente_id, total)
            nueva_venta_id = self.cur.fetchone()[0]
            self.con.commit()
            return nueva_venta_id
        except pyodbc.Error as e:
            print(f"Error al registrar la venta: {e}")
            return None
        finally:
            self.desconectar()

    def registrar_detalle_venta(self, venta_id, producto_id, cantidad, precio_unitario):
        """Registra un producto en el detalle de una venta."""
        if not self.conectar():
            return False
        try:
            sql = """
                INSERT INTO VentaDetalle (VentaID, ProductoID, Cantidad, PrecioUnitario) 
                VALUES (?, ?, ?, ?)
            """
            self.cur.execute(sql, venta_id, producto_id, cantidad, precio_unitario)
            self.con.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error al registrar el detalle de venta: {e}")
            return False
        finally:
            self.desconectar()
            
    def descontar_stock(self, producto_id, cantidad_vendida):
        """Actualiza el stock de un producto después de una venta."""
        if not self.conectar():
            return False
        try:
            sql = "UPDATE Producto SET Stock = Stock - ? WHERE ProductoID = ?"
            self.cur.execute(sql, cantidad_vendida, producto_id)
            self.con.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error al descontar stock: {e}")
            return False
        finally:
            self.desconectar()






