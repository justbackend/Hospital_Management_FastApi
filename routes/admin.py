from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import database
from functions.admin import register
from schemas.users import CreateUser
from fastapi import HTTPException

admin_router = APIRouter(
    prefix='/users'
)


@admin_router.post('/register')
async def register_user(form: CreateUser, db: Session = Depends(database)):
    register(form, db)
    return HTTPException(status_code=201, detail="Siz ro'yxatdan muvaffaqiyatli o'tdingiz")





