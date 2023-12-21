from pydantic import BaseModel, Field


class CreateTempPatient(BaseModel):
    name: str
    surname: str
    tolov: int = Field(..., gt=0)
    doctor: int


