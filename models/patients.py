from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Text
from utils.timezone import get_tashkent_time


class Patients(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    surname = Column(String(30))
    date = Column(DateTime, default=get_tashkent_time())
    desc = Column(Text, nullable=True)
    doctor = Column(Integer, ForeignKey("users.id"))
