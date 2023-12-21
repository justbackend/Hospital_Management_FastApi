from fastapi import WebSocket, WebSocketException, WebSocketDisconnect


class ConnectionManager:

    def __init__(self):
        self.doctors: dict[int, WebSocket] = {}
        self.screens: set[WebSocket] = set()
        self.checkboxes: set[WebSocket] = set()

    async def checkbox_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.checkboxes.add(websocket)

    async def doctor_connect(self, websocket: WebSocket, current_user_id):
        await websocket.accept()
        self.doctors[current_user_id] = websocket

    async def screen_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.screens.add(websocket)

    async def chechbox_disconnect(self, websocket):
        self.checkboxes.remove(websocket)

    async def screen_disconnect(self, websocket):
        self.screens.remove(websocket)

    async def doctor_disconnect(self, current_user_id):
        del self.doctors[current_user_id]

    async def checkbox_send(self, data):
        try:
            for checkbox in self.checkboxes:
                await checkbox.send_json(data)
        except WebSocketDisconnect:
            pass

    async def screen_send(self, data):
        for screen in self.screens:
            await screen.send_json(data)

    async def doctor_send(self, new_user, current_user_id):
        try:
            await self.doctors[current_user_id].send_json(new_user)
        except:
            pass


manager = ConnectionManager()
