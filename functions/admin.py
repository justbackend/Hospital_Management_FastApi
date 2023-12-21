from models.users import Users
from routes.login import get_password_hash


def register(form, db):
    new_user = Users(
        username=form.username,
        password_hash=get_password_hash(form.password_hash),
        surname=form.surname,
        room=form.room,
        field=form.field,
    )
    db.add(new_user)
    db.commit()
