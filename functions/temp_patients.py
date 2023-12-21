from fastapi import HTTPException

from functions.screen import all_queue
from models.temp_patients import TempPatients
from routes.websocket import manager
from fastapi.encoders import jsonable_encoder
from models.patients import Patients


async def add_patients(form, db):
    temp_patient = TempPatients(
        name=form.name,
        surname=form.surname,
        doctor=form.doctor,
        tolov=form.tolov
    )
    db.add(temp_patient)
    db.commit()
    patients = db.query(TempPatients).all()
    patients_doctor = db.query(TempPatients).filter(TempPatients.doctor == form.doctor).all()
    patients_json = jsonable_encoder(patients_doctor)
    await manager.doctor_send(patients_json, form.doctor)
    await manager.checkbox_send(jsonable_encoder(patients))


async def delete_patients(form, db, current_user):
    patient = db.query(TempPatients).filter(TempPatients.doctor == current_user.id).first()
    if patient is None:
        raise HTTPException(status_code=204, detail="Sizda hechqanday bemor yo'q")
    new_patient = Patients(
        name=patient.name,
        surname=patient.surname,
        desc=form.desc,
        doctor=patient.doctor
    )
    db.add(new_patient)
    db.delete(patient)
    db.commit()
    patients = db.query(TempPatients).filter(TempPatients.doctor == current_user.id).all()
    patients_json = jsonable_encoder(patients)
    await manager.doctor_send(patients_json, current_user.id)
    await manager.screen_send(await all_queue(db))


async def all_patients(db):
    patients = db.query(TempPatients).all()
    return jsonable_encoder(patients)


async def pay_patient(patient_id, db):
    patient = db.query(TempPatients).filter(TempPatients.id == patient_id).first()
    patient.status = True
    db.commit()
    patients = db.query(TempPatients).all()
    await manager.checkbox_send(jsonable_encoder(patients))

