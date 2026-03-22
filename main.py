from fastapi import FastAPI, HTTPException
import pyodbc

app = FastAPI(title="Mi API con SQL Server")

SERVER = 'TU_SERVIDOR_SQL'  # Cambia esto por el nombre de tu servidor valio vrga no me acuerdo como se llama
DATABASE = 'TU_BASE_DE_DATOS' # Cambia esto por el nombre de tu base de datos

def obtener_conexion(usuario, password):
    try:
        cadena = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={usuario};PWD={password}"
        return pyodbc.connect(cadena)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a la BD: {str(e)}")

@app.get("/clientes")
def listar_clientes():
    # Usamos antoconsulta solo para leer
    conexion = obtener_conexion('antoconsulta', 'tu_contraseña_aqui')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cliente")
    
    columnas = [columna[0] for columna in cursor.description]
    clientes = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    
    conexion.close()
    return clientes

@app.post("/clientes")
def registrar_cliente(nombre: str):
    # Se me ocurrio usar el usuario que creamos para la actividad de la profa 
    conexion = obtener_conexion('antoadmin', 'tu_contraseña_aqui')
    # Aquí la lógica de INSERT...
    conexion.close()
    return {"mensaje": f"Cliente {nombre} recibido. (Lógica de insert pendiente)"}