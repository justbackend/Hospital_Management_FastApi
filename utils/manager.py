from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from websockets.exceptions import ConnectionClosedError
from models import Users, Notification
from schemas import *


class ConnectionManager:

    def init(self):
        self.active_connections = []

    async def connect(self, websocket, user):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    async def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection[0] == websocket:
                self.active_connections.remove(connection)
                break

    async def send_personal_message(self, message: str, connection):
        websocket, user = connection
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            await self.disconnect(websocket)

    async def send_personal_json(self, message: NotificationSchema, connection):
        websocket, user = connection
        try:
            await websocket.send_json({
                "title": message.title,
                "body": message.body,
                "user_id": message.user_id
            })

        except WebSocketDisconnect:
            await self.disconnect(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            websocket, user = connection
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                await self.disconnect(websocket)

    async def broadcast_json(self, message):
        for connection in self.active_connections:
            websocket, user = connection
            try:
                await websocket.send_json(message)
            except WebSocketDisconnect:
                await self.disconnect(websocket)
            except ConnectionClosedError as xatolik:
                print(xatolik)

    async def send_user(self, message, user_id, db):

        sent = False
        for connection in self.active_connections:
            websocket, user = connection
            try:
                if user.id == user_id:
                    await websocket.send_json({
                        "title": message.title,
                        "body": message.body,
                        "user_id": message.user_id,
                    })
                    sent = True
            except WebSocketDisconnect:
                await self.disconnect(websocket)

        if sent == False:
            db.add(Notification(
                title=message.title,
                body=message.body,
                user_id=message.user_id
            ))
            db.commit()

        return sent


manager = ConnectionManager()
