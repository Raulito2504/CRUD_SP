from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# LIFESPAN (reemplaza @app.on_event deprecated)
# ─────────────────────────────────────────
def _probar_conexion() -> bool:
    """Intenta conectarse a SQL Server usando las variables del .env."""
    try:
        pwd = os.getenv('DB_PASS', '')
        cadena = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={{{pwd}}}"   # las llaves {} escapan caracteres especiales como ; en ODBC
        )
        con = pyodbc.connect(cadena, timeout=5)
        con.close()
        return True
    except Exception as e:
        logger.error(f"Error de conexión a SQL Server: {e}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──
    logger.info("Iniciando aplicación...")
    if _probar_conexion():
        logger.info("GG Conexión a SQL Server exitosa.")
    else:
        logger.warning("FF No se pudo conectar a SQL Server. Revisa tu .env.")
    yield
    # ── SHUTDOWN ──
    logger.info("Cerrando aplicación...")


# ─────────────────────────────────────────
# INSTANCIA FASTAPI
# ─────────────────────────────────────────
app = FastAPI(
    title="Mi API con Stored Procedures",
    description="API REST que consume SP's de SQL Server",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ─────────────────────────────────────────
# CORS
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # En producción: especifica dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
# MANEJADOR GLOBAL DE ERRORES
# ─────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error no controlado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Contacta al administrador."},
    )


# ─────────────────────────────────────────
# ROUTERS  →  agrega aquí tus módulos
# ─────────────────────────────────────────
# from app.api.routes import items
# app.include_router(items.router, prefix="/api/v1/items", tags=["Items"])


# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────
@app.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok", "version": app.version}


# ─────────────────────────────────────────
# DB TEST
# ─────────────────────────────────────────
@app.get("/db-test", tags=["Status"])
def db_test():

    if _probar_conexion():
        return {
            "status": "ok",
            "message": "Conexión a SQL Server exitosa V",
            "server": os.getenv("DB_SERVER"),
            "database": os.getenv("DB_NAME"),
        }
    return JSONResponse(
        status_code=503,
        content={
            "status": "error",
            "message": "No se pudo conectar a SQL Server X. Revisa tu .env y que el servidor esté activo.",
        },
    )