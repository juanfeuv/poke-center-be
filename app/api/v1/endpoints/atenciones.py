import traceback
import time

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.deps import get_current_user
from app.database.crud.crud_atenciones import CRUDAtenciones
from app.api.v1.global_import import FastApiResponse
from pydantic import BaseModel
from typing import Optional


router = APIRouter()


class Atencion(BaseModel):
    hp: int
    trainer_name: str
    trainer_id: str
    cambio_estado: dict = {}
    nivel: int
    pokemon_name: str
    pokemon_id: int
    pokemon_info: dict = {}

class Prioridad(BaseModel):
    id: int
    turn_number: int

class Atender(BaseModel):
    id: int
    estado: str = "atender"
    comment: str = ""

class AtencionesResults(BaseModel):
    hp: Optional[int] = None
    trainerName: Optional[str] = None
    trainerId: Optional[str] = None
    cambioEstado: Optional[dict] = None
    nivel: Optional[int] = None
    pokemonName: Optional[str] = None
    createdAt: Optional[str] = None
    pokemonId: Optional[int] = None
    pokemonInfo: Optional[dict] = None
    turnNumber: Optional[int] = None
    id: Optional[int] = None
    estado: Optional[str] = None
    comment: Optional[str] = None
    fechaAtencion: Optional[str] = None


@router.post('/crear-atencion')
def crear_atencion(atencion: Atencion, current_user=Depends(get_current_user)):

    try:
        user_id = current_user.get("user_id")
        id_generated = int(time.time() * 1000)
        CRUDAtenciones.create_object(hp=atencion.hp,
                                     trainer_name=atencion.trainer_name,
                                     trainer_id=atencion.trainer_id,
                                     cambio_estado=atencion.cambio_estado,
                                     nivel=atencion.nivel,
                                     pokemon_name=atencion.pokemon_name,
                                     pokemon_id=atencion.pokemon_id,
                                     pokemon_info=atencion.pokemon_info,
                                     raw_id=id_generated,
                                     user_id=user_id)

        return { "id": id_generated }

    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))


@router.post('/bajar-prioridad')
def bajar_prioridad(prioridad: Prioridad, current_user=Depends(get_current_user)):
    try:
        payload = { "turnNumber": prioridad.turn_number }

        CRUDAtenciones.update_turn_by_id(raw_id=prioridad.id, payload=payload)

        return FastApiResponse.successful

    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))
    

@router.post('/atender')
def atender(atender: Atender, current_user=Depends(get_current_user)):
    try:
        payload = {
            "estado": atender.estado,
            "comment": atender.comment,
            "fechaAtencion": datetime.now()
            }

        CRUDAtenciones.update_turn_by_id(raw_id=atender.id, payload=payload)

        return FastApiResponse.successful

    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))
    

@router.get('/get-atenciones')
def get_atenciones(atendidos="false", current_user=Depends(get_current_user)):
    try:
        list_of_fields = ["hp", "trainerName", "trainerId", "cambioEstado", "nivel", "pokemonName", "createdAt", "pokemonId", "pokemonInfo", "turnNumber", "estado", "comment", "fechaAtencion"]
        new_items = []
        result = CRUDAtenciones.get_items(atendidos=atendidos)
        for obt in result:
            item = {}
            item["id"] = obt.get("rawId")
            for field in list_of_fields:
                item[field] = obt.get(field)
            
            new_items.append(item)

        return new_items

    except Exception as e:
        print(f"Error: {e}", traceback.format_exc())
        return FastApiResponse.failure(str(e))
