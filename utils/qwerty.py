from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from database import SessionLocal, database
from jose import jwt
from models import Users, Notification, Sms
from .notification import manager
from .sms import manager as sms_manager
from schemas import NotificationSchema, SmsSchema
from .login import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session

notification_router = APIRouter()


@notification_router.websocket("/ws/connection")
async def websocket_endpoint(
        token: str,
        status: str,
        websocket: WebSocket,
        db: Session = Depends(database)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    user: Users = db.query(Users).filter_by(username=username, status=True).first()
    if status == "notification":
        await manager.connect(websocket, user)
        if user:
            for ntf in user.notifications:
                message = NotificationSchema(
                    title=ntf.title,
                    body=ntf.body,
                    user_id=ntf.user_id,

                )
                await manager.send_personal_json(message, (websocket, user))
            db.query(Notification).filter_by(user_id=user.id).delete()
            db.commit()
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
    elif status == "sms":
        await sms_manager.connect(websocket, user)
        if user:
            for ntf in user.smslar:
                message = SmsSchema(
                    title=ntf.title,
                    text=ntf.text,
                    phone=ntf.phone,
                    date=ntf.date,
                    branch_id=ntf.branch_id,
                    user_id=ntf.user_id,

                )
                await sms_manager.send_personal_json(message, (websocket, user))
            db.query(Sms).filter_by(user_id=user.id).delete()
            db.commit()
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await sms_manager.disconnect(websocket)