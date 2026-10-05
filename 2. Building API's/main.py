from fastapi import FastAPI, HTTPException
from Pydantic_model.Model_Validation import Student
from typing import List

students_db: List[Student] = []

app = FastAPI()


@app.get('/Students', response_model=List[Student])
def get_students():
    return students_db


@app.get('/Students/{stud_id}', response_model=Student)
def get_student(stud_id: int):
    for index,student in enumerate(students_db):
        if student.id == stud_id:
            return students_db[index]
    raise HTTPException(status_code=404, detail='Student not found')

 
@app.post('/Add_Student')
def add_student(new_stud: Student):
    for student in students_db:
        if student.id == new_stud.id:
            raise HTTPException(status_code=400, detail='Student already exists')
    students_db.append(new_stud)
    return {'Message':'Add new student Successfully'}


@app.put('/Update_Student/{stud_id}')
def update_student(stud_id: int, updated_student: Student):
    for index, student in enumerate(students_db):
        if student.id == stud_id:
            students_db[index] = updated_student
            return {'Message':'Updated student Successfully'}
    raise HTTPException(status_code=404, detail='Employee Not Found')

@app.delete('/delete_student/{stud_id}')
def delete_student(stud_id: int):
    for index, student in enumerate(students_db):
        if student.id == stud_id:
            del students_db[index]
            return {'message': 'Student deleted successfully'}
    raise HTTPException(status_code=404, detail='Student Not Found')