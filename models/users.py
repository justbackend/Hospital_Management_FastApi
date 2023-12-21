from database import Base
from sqlalchemy import Column, String, Integer


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(30), nullable=True)
    surname = Column(String(30))
    field = Column(String(20))
    room = Column(String(10), unique=True, nullable=False)
    role = Column(String(20), default="user")
    token = Column(String(255), nullable=True)
