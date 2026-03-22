from db.connection import get_connection
from schemas.cliente import ClienteCreate, ClienteUpdate


def get_all_clientes():
    """Llama a sp_GetClientes y devuelve la lista completa."""
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute("EXEC sp_GetClientes")
        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall()

    return [dict(zip(columnas, fila)) for fila in filas]


def get_cliente_by_id(id: int):
    """Llama a sp_GetClienteById. Retorna el cliente o None si no existe."""
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute("EXEC sp_GetClienteById @id = ?", id)
        columnas = [col[0] for col in cursor.description]
        fila = cursor.fetchone()

    if fila is None:
        return None
    return dict(zip(columnas, fila))


def create_cliente(data: ClienteCreate):
    """Llama a sp_InsertCliente y retorna el id generado."""
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(
            "EXEC sp_InsertCliente @nombre=?, @apellido1=?, @apellido2=?, @ciudad=?, @categoria=?",
            data.nombre, data.apellido1, data.apellido2, data.ciudad, data.categoria
        )
        nuevo_id = cursor.fetchone()[0]
        con.commit()

    return nuevo_id


def update_cliente(id: int, data: ClienteUpdate):
    """Llama a sp_UpdateCliente. Retorna True si encontró el registro, False si no."""
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute(
            "EXEC sp_UpdateCliente @id=?, @nombre=?, @apellido1=?, @apellido2=?, @ciudad=?, @categoria=?",
            id, data.nombre, data.apellido1, data.apellido2, data.ciudad, data.categoria
        )
        filas_afectadas = cursor.fetchone()[0]
        con.commit()

    return filas_afectadas > 0


def delete_cliente(id: int):
    """Llama a sp_DeleteCliente. Retorna True si encontró el registro, False si no."""
    with get_connection() as con:
        cursor = con.cursor()
        cursor.execute("EXEC sp_DeleteCliente @id = ?", id)
        filas_afectadas = cursor.fetchone()[0]
        con.commit()

    return filas_afectadas > 0
