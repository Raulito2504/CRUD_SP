# ¿Cómo funciona esta API? — Guía paso a paso

## El flujo completo (de afuera hacia adentro)

```
Petición HTTP (Postman / Swagger)
        ↓
  api/routes/         → ¿A qué endpoint llego?
        ↓
  services/           → ¿Qué lógica ejecuto?
        ↓
  db/connection.py    → Abro la conexión a SQL Server
        ↓
  SQL Server          → Ejecuta el Stored Procedure
        ↓
  (respuesta sube el mismo camino de vuelta)
```

---

## Cada carpeta explicada con el ejemplo del CRUD

### 📁 `schemas/cliente.py`
**¿Qué es?** Los contratos de datos. Define exactamente qué campos entran y salen.

```python
class ClienteCreate(BaseModel):
    nombre:    str           # obligatorio
    apellido1: str           # obligatorio
    apellido2: Optional[str] # opcional (puede venir vacío)
    ciudad:    Optional[str]
    categoria: Optional[int]
```

Cuando haces un `POST`, FastAPI usa este modelo para **validar automáticamente** el JSON que mandes.
Si mandas un campo mal (por ej. `categoria: "hola"` en vez de un número), FastAPI rechaza la petición antes de que llegue al service.

> **Regla:** `ClienteCreate` = lo que recibes. `ClienteResponse` = lo que devuelves (incluye el `id`).

---

### 📁 `services/clientes.py`
**¿Qué es?** La capa de lógica. Aquí se llama a cada Stored Procedure.

```python
def create_cliente(data: ClienteCreate):
    with get_connection() as con:      # 1. Pide una conexión
        cursor = con.cursor()
        cursor.execute(                # 2. Llama al SP con parámetros
            "EXEC sp_InsertCliente @nombre=?, ...",
            data.nombre, data.apellido1, ...
        )
        nuevo_id = cursor.fetchone()[0]  # 3. Lee el resultado
        con.commit()                     # 4. Confirma la transacción
    return nuevo_id                      # 5. Devuelve el dato al route
```

El `with get_connection() as con:` cierra la conexión **automáticamente** al terminar, aunque ocurra un error.

> **Regla:** El service no sabe nada de HTTP. Solo recibe datos, llama al SP y devuelve resultados.

---

### 📁 `api/routes/clientes.py`
**¿Qué es?** La puerta de entrada HTTP. Define los endpoints y nada más.

```python
@router.post("/", response_model=dict, status_code=201)
def create_cliente(data: ClienteCreate):
    nuevo_id = service.create_cliente(data)   # delega al service
    return {"message": "Cliente creado", "id": nuevo_id}
```

Nota que el route **no toca la base de datos**. Solo:
1. Recibe la petición
2. Llama al service
3. Devuelve la respuesta

> **Regla:** Si el service retorna `None` o `False` (no encontró el registro), el route lanza un `404`.

---

### 📁 `db/connection.py`
**¿Qué es?** El único lugar que sabe cómo conectarse a SQL Server.

```python
def get_connection() -> pyodbc.Connection:
    cadena = get_connection_string()   # lee las variables del .env
    return pyodbc.connect(cadena)
```

Si mañana cambias de SQL Server a PostgreSQL, **solo cambias este archivo**. El resto del código no se toca.

---

### 📁 `core/config.py`
**¿Qué es?** Configuración global (variables de entorno, settings de la app).
Usa `pydantic-settings` para cargar y validar las variables del `.env` con tipos.

---

### 📄 `main.py`
**¿Qué es?** El punto de entrada de toda la aplicación. Hace 3 cosas:

1. **Crea la app FastAPI** con su configuración
2. **Registra los routers** (aquí conectas tus módulos)
3. **Maneja el arranque/apagado** (verifica la conexión a DB al iniciar)

```python
# Así se "activa" un nuevo módulo en la API
from api.routes import clientes
app.include_router(clientes.router, prefix="/api/v1")
```

---

## ¿Cómo agrego otro CRUD mañana?

Si mañana tuvieras una tabla `producto`, el proceso sería siempre el mismo:

| Paso | Archivo | Qué haces |
|------|---------|-----------|
| 1 | `database/sp_usados.sql` | Creas los 5 SPs en SQL Server |
| 2 | `schemas/producto.py` | Defines los modelos Pydantic |
| 3 | `services/productos.py` | Ejecutas los SPs |
| 4 | `api/routes/productos.py` | Defines los endpoints |
| 5 | `main.py` | Registras el router |

---

## Resumen visual

```
.env
 └── DB_SERVER, DB_NAME, DB_USER, DB_PASS
        ↓ lo lee
db/connection.py
        ↓ lo usa
services/clientes.py  ←→  SQL Server (Stored Procedures)
        ↓ lo usa
api/routes/clientes.py
        ↓ registrado en
main.py  →  http://127.0.0.1:8000/api/v1/clientes/
```
