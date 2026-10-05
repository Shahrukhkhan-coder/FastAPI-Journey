from sqlalchemy.orm import Session
import models, schemas

def get_students(db: Session):
    return db.query(models.Student_table).all()


def get_student(db: Session, roll_no:int):
    return db.query(models.Student_table).filter(models.Student_table.Roll_no == roll_no).first()

def create_student(db:Session, student: schemas.Student):
    db_student = models.Student_table(
        Roll_no = student.Roll_no,
        Name = student.Name,
        Address = student.Address
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, roll_no: int, student: schemas.Student):
    db_student = db.query(models.Student_table).filter(models.Student_table.Roll_no == roll_no).first()
    if db_student:
        db_student.Roll_no = student.Roll_no
        db_student.name = student.Name
        db_student.Address = student.Address
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, roll_no: int):
    db_student= db.query(models.Student_table).filter(models.Student_table.Roll_no == roll_no).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student