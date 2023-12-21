from models.temp_patients import TempPatients
from fastapi.encoders import jsonable_encoder


async def get_patients(db, current_user):
    patients = db.query(TempPatients).filter(TempPatients.doctor == current_user.id, TempPatients.status == True).all()
    return jsonable_encoder(patients)
