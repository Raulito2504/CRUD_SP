from fastapi import APIRouter, HTTPException
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from services import clientes as service

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteResponse])
def get_clientes():
    """Obtiene todos los clientes."""
    return service.get_all_clientes()


@router.get("/{id}", response_model=ClienteResponse)
def get_cliente(id: int):
    """Obtiene un cliente por su id."""
    cliente = service.get_cliente_by_id(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=dict, status_code=201)
def create_cliente(data: ClienteCreate):
    """Crea un nuevo cliente."""
    nuevo_id = service.create_cliente(data)
    return {"message": "Cliente creado exitosamente", "id": nuevo_id}


@router.put("/{id}", response_model=dict)
def update_cliente(id: int, data: ClienteUpdate):
    """Actualiza todos los campos de un cliente."""
    encontrado = service.update_cliente(id, data)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente actualizado exitosamente"}


@router.delete("/{id}", response_model=dict)
def delete_cliente(id: int):
    """Elimina un cliente por su id."""
    encontrado = service.delete_cliente(id)
    if not encontrado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado exitosamente"}
