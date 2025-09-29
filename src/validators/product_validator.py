class ProductoValidator:
    """Validador para datos de productos"""
    
    @staticmethod
    def validar_producto(codigo, descripcion, cantidad_str, precio_str):
        """Valida los datos de un producto y retorna lista de errores"""
        errores = []
        
        # Validar código
        if not codigo or not codigo.strip():
            errores.append("El código del producto es requerido")
        
        # Validar descripción
        if not descripcion or not descripcion.strip():
            errores.append("La descripción del producto es requerida")
        
        # Validar precio
        try:
            precio = float(precio_str)
            if precio < 0:
                errores.append("El precio no puede ser negativo")
        except (ValueError, TypeError):
            errores.append("El precio debe ser un número válido")
        
        # Validar cantidad
        try:
            cantidad = int(cantidad_str)
            if cantidad < 0:
                errores.append("La cantidad no puede ser negativa")
        except (ValueError, TypeError):
            errores.append("La cantidad debe ser un número entero válido")
        
        return errores
