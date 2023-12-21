from fastapi import HTTPException


async def role_verification(user):
    # allowed_functions_for_admins = []

    if user.role in ["admin", "user"]:
        return True

    raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def is_admin(user):
    if user.role != 'admin':
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


def is_user(user):
    if user.role != 'user':
        raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')


