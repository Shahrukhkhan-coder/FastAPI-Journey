import models, schemas, crud
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from typing import List


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/admit_student', response_model=schemas.Student)
def admit_student(student: schemas.Student, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get('/View_students', response_model=List[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get('/View_student/{roll_no}', response_model=schemas.Student)
def get_student(roll_no: int, db: Session = Depends(get_db)):
    student_record = crud.get_student(db, roll_no)
    if student_record is None:
         raise HTTPException(status_code=404, detail='Student record Not Found')
    return student_record

@app.put('/updated_record/{roll_no}', response_model=schemas.Student)
def update_student(roll_no: int, student: schemas.Student, db: Session = Depends(get_db)):
    student_record = crud.update_student(db, roll_no, student)
    if student_record is None:
         raise HTTPException(status_code=404, detail='Student record Not Found')
    return student_record


@app.delete('/delete_record/{roll_no}', response_model=dict)
def delete_student(roll_no: int, db: Session = Depends(get_db)):
    student_record = crud.delete_student(db, roll_no)
    if student_record is None:
        raise HTTPException(status_code=404, detail='Student_record Not Found')
    return {'Message': 'student_record Deleted'}

