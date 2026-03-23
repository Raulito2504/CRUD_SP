import logging
import pyodbc
from core.config import settings

logger = logging.getLogger(__name__)


def get_connection_string() -> str:
    """Construye la cadena de conexión ODBC """
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={settings.DB_SERVER};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={{{settings.DB_PASS}}}"   # las llaves {} escapan caracteres especiales como ; en ODBC
    )


def get_connection() -> pyodbc.Connection:
    """
    Abre y retorna una conexión activa a SQL Server
    """
    cadena = get_connection_string()
    return pyodbc.connect(cadena)


def probar_conexion() -> bool:
    """
    Verifica si es posible establecer una conexión a SQL Server.
    """
    try:
        con = pyodbc.connect(get_connection_string(), timeout=5)
        con.close()
        return True
    except Exception as e:
        logger.error(f"Error de conexión a SQL Server: {e}")
        return False
