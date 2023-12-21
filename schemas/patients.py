from pydantic import BaseModel, Field
from typing import Optional


class CreatePatient(BaseModel):
    desc: Optional[str] = Field(None)


class UpdatePatient(BaseModel):
    id: int
    desc: str
