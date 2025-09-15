# Sistema de Ventas con Python y Flask

Este es un proyecto de sistema de gestión de ventas basado en la web, desarrollado con el micro-framework Flask en Python. La aplicación está actualmente en un proceso de refactorización y mejora para seguir las mejores prácticas de desarrollo de software.

---

## Mejoras Realizadas (Refactorización)

Como parte de la modernización del proyecto, se han implementado varias mejoras significativas en la estructura, seguridad y eficiencia del código. A continuación se detallan los cambios realizados:

### 1. Seguridad y Gestión de Entorno

*   **¿Qué se hizo?**: Se eliminó toda la información sensible (credenciales de la base de datos, `secret_key` de Flask) que estaba escrita directamente en el código fuente. Ahora, estos valores se gestionan a través de un archivo `.env` y se cargan en la aplicación como variables de entorno.
*   **¿Por qué?**: Esta es la mejora más crítica. Escribir contraseñas y claves en el código (`hardcoding`) es una vulnerabilidad de seguridad grave. Si el código se sube a un repositorio público como GitHub, cualquiera podría ver las credenciales y atacar la base de datos. El uso de un archivo `.env` (ignorado por Git gracias al `.gitignore`) aísla los secretos del código fuente, siguiendo las mejores prácticas de la industria.

### 2. Estructura del Proyecto con Blueprints

*   **¿Qué se hizo?**: Se migró de una estructura monolítica (todo en un solo archivo `app.py`) a una arquitectura modular utilizando **Blueprints** de Flask. Se creó una carpeta `src` que ahora contiene la lógica de la aplicación separada en:
    *   `auth.py`: Un blueprint para las rutas de autenticación (`/login`, `/logout`).
    *   `main.py`: Un blueprint para las rutas generales de la aplicación.
    *   `__init__.py`: Contiene la **fábrica de la aplicación** (`create_app`), que se encarga de ensamblar la app, registrar los blueprints y configurar todo.
*   **¿Por qué?**: A medida que una aplicación crece, un solo archivo se vuelve caótico y difícil de mantener. La estructura con Blueprints organiza el código por funcionalidad, haciendo el proyecto más escalable, legible y fácil para trabajar en equipo.

### 3. Optimización de Plantillas HTML (Templates)

*   **¿Qué se hizo?**: Se creó una plantilla base (`templates/base.html`) que contiene la estructura HTML común (doctype, head, body, scripts). Las plantillas existentes (`login.html`, `construccion.html`) ahora **heredan** de esta base, insertando su contenido específico en bloques definidos. Adicionalmente, se integró el framework **Bootstrap 5** para mejorar la interfaz de usuario.
*   **¿Por qué?**: Esto sigue el principio **DRY (Don't Repeat Yourself - No te repitas)**. Evita la duplicación de código en los archivos HTML, facilita la realización de cambios de diseño globales (modificando solo `base.html`) y mejora la consistencia visual de la aplicación. La integración de Bootstrap proporciona un diseño moderno y responsivo con mínimo esfuerzo.

---

## Stack de Tecnologías

*   **Backend**: Python, Flask
*   **Base de Datos**: MySQL
*   **Frontend**: HTML, CSS, Bootstrap 5
*   **Gestión de Entorno**: `python-dotenv`

---

## Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

**1. Clonar el Repositorio**
```bash
git clone <URL_DEL_REPOSITORIO_EN_GITHUB>
cd Python-sistema-ventas
```

**2. Crear y Activar un Entorno Virtual**
*En Windows:*
```bash
python -m venv venv
.\venv\Scripts\activate
```

**3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar las Variables de Entorno**
Crea un archivo llamado `.env` en la raíz del proyecto (`Python-sistema-ventas/.env`). Copia y pega el siguiente contenido, reemplazando los valores si es necesario.

```ini
# Archivo .env.example
# No uses comillas para los valores

FLASK_SECRET_KEY=una_clave_muy_secreta_y_larga
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_de_mysql
DB_NAME=sistemaventa
```

**5. Ejecutar la Aplicación**
```bash
flask run
# O también:
# python app.py
```

La aplicación estará corriendo en `http://127.0.0.1:5000`.