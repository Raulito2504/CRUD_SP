```
# CRUD_SP

API RESTful construida con FastAPI y conectada a SQL Server.

## Configuración y ejecución

Sigue estos pasos en tu terminal para levantar la API en tu entorno local:

### 1. Crear el entorno virtual
Crea un entorno aislado para no mezclar librerías con tu sistema:
```bash
python -m venv .venv
```

### 2. Activar el entorno
Asegúrate de ver `(.venv)` al inicio de tu terminal después de ejecutar esto:
```bash
.\.venv\Scripts\activate
```

### 3. Instalar dependencias
Descarga todas las herramientas necesarias de un solo golpe:
```bash
pip install -r requirements.txt
```

### 4. Arrancar el servidor
Inicia la API con recarga automática para desarrollo:
```bash
uvicorn main:app --reload
```

## Pruebas

Una vez que el servidor esté corriendo, abre tu navegador en la siguiente dirección para ver la documentación interactiva:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
```

JEFFREY EIPSTEN
