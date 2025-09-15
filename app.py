from src import create_app

# Crea la instancia de la aplicación llamando a la fábrica
app = create_app()

# Ejecuta la aplicación
if __name__ == '__main__':
    # Se recomienda usar host='0.0.0.0' para que sea accesible en la red local
    app.run(host='0.0.0.0', port=5000, debug=True)
