"""
Router para el sistema de puntos de fidelidad

Este router maneja la acumulación y canje de puntos
para los clientes del negocio de estética.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database.Clever_MySQL_conn import cleverCursor, mysqlConn
from datetime import datetime
from typing import List, Optional

puntosRouter = APIRouter()

# Modelos

class PuntosBase(BaseModel):
    """Modelo base para puntos de fidelidad"""
    puntos_acumulados: int
    puntos_restantes: int

class CanjeBase(BaseModel):
    """Modelo base para canjes de puntos"""
    puntos_canjeados: int
    premio: str

# Rutas

@puntosRouter.get("/{id_cliente}", status_code=status.HTTP_200_OK)
def obtener_puntos_cliente(id_cliente: int):
    """
    Obtener puntos de un cliente
    Retorna la información de puntos del cliente
    """
    try:
        cleverCursor.execute(
            "SELECT * FROM puntos WHERE id_cliente = %s", (id_cliente,)
        )
        puntos = cleverCursor.fetchone()
        if not puntos:
            raise HTTPException(status_code=404, detail="Cliente no tiene puntos registrados")
        return puntos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener puntos: {e}")

@puntosRouter.post("/acumular", status_code=status.HTTP_201_CREATED)
def acumular_puntos(id_cliente: int, puntos: int):
    """
    Acumular puntos para un cliente
    Actualiza el saldo de puntos del cliente
    """
    try:
        # Verificar si el cliente tiene puntos registrados
        cleverCursor.execute(
            "SELECT * FROM puntos WHERE id_cliente = %s", (id_cliente,)
        )
        puntos_existentes = cleverCursor.fetchone()
        
        if puntos_existentes:
            # Actualizar puntos existentes
            nuevos_puntos = puntos_existentes[2] + puntos
            update_query = """
            UPDATE puntos 
            SET puntos_acumulados = puntos_acumulados + %s,
                puntos_restantes = puntos_restantes + %s,
                fecha_actualizacion = NOW()
            WHERE id_cliente = %s
            """
            cleverCursor.execute(update_query, (puntos, puntos, id_cliente))
        else:
            # Crear nuevo registro de puntos
            insert_query = """
            INSERT INTO puntos (id_cliente, puntos_acumulados, puntos_restantes)
            VALUES (%s, %s, %s)
            """
            cleverCursor.execute(insert_query, (id_cliente, puntos, puntos))
        
        mysqlConn.commit()
        return {"message": "Puntos acumulados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al acumular puntos: {e}")

@puntosRouter.post("/canjear", status_code=status.HTTP_201_CREATED)
def canjear_puntos(id_cliente: int, canje: CanjeBase):
    """
    Canjear puntos por un premio
    Verifica si el cliente tiene suficientes puntos
    y realiza el canje si es posible
    """
    try:
        # Verificar puntos disponibles
        cleverCursor.execute(
            "SELECT * FROM puntos WHERE id_cliente = %s", (id_cliente,)
        )
        puntos = cleverCursor.fetchone()
        
        if not puntos or puntos[3] < canje.puntos_canjeados:
            raise HTTPException(status_code=400, detail="Puntos insuficientes para el canje")
        
        # Registrar el canje
        insert_canje = """
        INSERT INTO canjes (id_puntos, puntos_canjeados, premio)
        VALUES (%s, %s, %s)
        """
        cleverCursor.execute(insert_canje, (puntos[0], canje.puntos_canjeados, canje.premio))
        
        # Actualizar puntos restantes
        update_puntos = """
        UPDATE puntos 
        SET puntos_restantes = puntos_restantes - %s,
            fecha_actualizacion = NOW()
        WHERE id_cliente = %s
        """
        cleverCursor.execute(update_puntos, (canje.puntos_canjeados, id_cliente))
        
        mysqlConn.commit()
        return {"message": "Canje realizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar canje: {e}")
