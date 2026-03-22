import os
import logging
import pyodbc
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_connection_string() -> str:
    """Construye la cadena de conexión ODBC a partir de las variables de entorno."""
    pwd = os.getenv("DB_PASS", "")
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={{{pwd}}}"   # las llaves {} escapan caracteres especiales como ; en ODBC
    )


def get_connection() -> pyodbc.Connection:
    """
    Abre y retorna una conexión activa a SQL Server.
    El llamador es responsable de cerrarla (usar con 'with' o .close()).
    """
    cadena = get_connection_string()
    return pyodbc.connect(cadena)


def probar_conexion() -> bool:
    """
    Verifica si es posible establecer una conexión a SQL Server.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        con = pyodbc.connect(get_connection_string(), timeout=5)
        con.close()
        return True
    except Exception as e:
        logger.error(f"Error de conexión a SQL Server: {e}")
        return False
