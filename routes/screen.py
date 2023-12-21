from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import database
from functions.screen import all_queue
from routes.login import get_current_user_socket
from routes.websocket import manager
from schemas.users import UserCurrent
from utils.role_verification import role_verification


screen_router = APIRouter(prefix='/screen')


@screen_router.websocket('/ws')
async def get_queue(websocket: WebSocket, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user_socket)):
    await role_verification(current_user)
    await manager.screen_connect(websocket)
    await websocket.send_json(await all_queue(db))
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            await manager.screen_disconnect(websocket)
