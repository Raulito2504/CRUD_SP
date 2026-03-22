from pydantic import BaseModel
from typing import Optional


# ── Lo que se necesita para CREAR un cliente ──────────────────
class ClienteCreate(BaseModel):
    nombre:    str
    apellido1: str
    apellido2: Optional[str] = None
    ciudad:    Optional[str] = None
    categoria: Optional[int] = None


# ── Lo que se necesita para ACTUALIZAR un cliente ─────────────
class ClienteUpdate(BaseModel):
    nombre:    str
    apellido1: str
    apellido2: Optional[str] = None
    ciudad:    Optional[str] = None
    categoria: Optional[int] = None


# ── Lo que la API devuelve al cliente (incluye el id) ─────────
class ClienteResponse(BaseModel):
    id:        int
    nombre:    str
    apellido1: str
    apellido2: Optional[str] = None
    ciudad:    Optional[str] = None
    categoria: Optional[int] = None
