from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import database
from functions.temp_patients import add_patients, delete_patients, all_patients, pay_patient
from routes.login import get_current_user, get_current_user_socket
from routes.websocket import manager
from schemas.patients import CreatePatient
from schemas.users import UserCurrent
from schemas.temp_patients import CreateTempPatient
from utils.role_verification import is_admin

temp_patients_router = APIRouter(
    prefix='/temp_patients'
)


@temp_patients_router.post('/add_queue')
async def patients_add(form: CreateTempPatient, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user)):
    is_admin(current_user)
    await add_patients(form, db)
    return HTTPException(status_code=201, detail="Bemor navbatga muvaffaqiyatli qo'shildi")


@temp_patients_router.websocket("/ws")
async def get_patietns(websocket: WebSocket, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user_socket)):
    is_admin(current_user)
    await manager.checkbox_connect(websocket)
    await manager.checkbox_send(await all_patients(db))
    while True:
        try:
            await websocket.receive_text()
        except WebSocketDisconnect:
            await manager.chechbox_disconnect(websocket)


@temp_patients_router.post('/pay_money')
async def patient_pay(patient_id: int, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user)):
    is_admin(current_user)
    await pay_patient(patient_id, db)
    return HTTPException(status_code=200, detail="To'lov qabul qilindi")


@temp_patients_router.post('/delete')
async def patients_delete(form: CreatePatient, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_user)):
    await delete_patients(form, db, current_user)
    return HTTPException(status_code=200, detail="Bu mijoz muvaffaqiyatli o'chirildi")




