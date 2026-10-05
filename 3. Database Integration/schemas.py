from pydantic import BaseModel, Field


class Student(BaseModel):
    Roll_no : int = Field(..., gt=0)
    Name : str
    Address : str


class Config:
    from_attributes = True