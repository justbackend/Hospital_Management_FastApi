from fastapi import APIRouter, Depends, WebSocket, WebSocketException, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database import database
from functions.users import get_patients
from models.temp_patients import TempPatients
from routes.login import get_current_user, get_current_user_socket
from schemas.users import UserCurrent
from utils.role_verification import role_verification
from .websocket import manager
users_router = APIRouter(prefix='/users')


@users_router.websocket('/ws')
async def patients_get(websocket: WebSocket, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user_socket)):
    await manager.doctor_connect(websocket, current_user.id)
    await websocket.send_json(await get_patients(db, current_user))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.doctor_disconnect(current_user.id)



