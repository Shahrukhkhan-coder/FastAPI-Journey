from sqlalchemy import Column, Integer, String
from database import Base


class Student_table(Base):
    __tablename__ = 'Student_Info'
    Roll_no = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Address = Column(String, index=True)