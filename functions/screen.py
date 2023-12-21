from models.temp_patients import TempPatients
from models.users import Users
from fastapi.encoders import jsonable_encoder


async def all_queue(db):
    json_queue = {}
    all_patients = db.query(TempPatients).filter(TempPatients.status==True).all()
    all_doctors = db.query(Users).filter(Users.role == "user").all()
    for doctor in all_doctors:
        for patient in all_patients:
            if patient.doctor == doctor.id:
                json_queue[doctor.room] = patient.name
                break
    return jsonable_encoder(json_queue)