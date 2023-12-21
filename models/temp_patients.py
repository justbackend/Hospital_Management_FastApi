from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


class TempPatients(Base):
    __tablename__ = "temp_patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    surname = Column(String(30))
    tolov = Column(Integer)
    status = Column(Boolean, default=False)
    doctor = Column(Integer, ForeignKey("users.id"))

