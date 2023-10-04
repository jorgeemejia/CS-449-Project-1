import collections
import contextlib
import logging.config
import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status, Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

class Drop(BaseModel):
    StudentID: int
    ClassID: int


# class Book(BaseModel):
#     published: int
#     author: str
#     title: str
#     first_sentence: str
class Enrollment(BaseModel):
    StudentID: int
    ClassID: int

class Instructor(BaseModel):
    InstructorID: int
    FirstName: str
    LastName: str

class Classes(BaseModel):
    ClassID: int
    ClassSectionNumber: int
    CourseID: int
    InstructorID: int
    MaxClassEnrollment: int

class Student(BaseModel):
    StudentID: int
    FirstName: str
    LastName: str




def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db


def get_logger():
    return logging.getLogger(__name__)


settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers=False)

@app.get("/")
def hello_world():
    return {"Up and running"}

@app.delete("/student/class/drop/{StudentID}/{ClassID}")
def drop_student_from_class(StudentID: int, ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM enrollments WHERE StudentID = ? AND ClassID = ?', (StudentID, ClassID))
        cursor.execute("INSERT INTO droplists (StudentID, ClassID, AdminDrop) VALUES (?, ?, ?)", (StudentID, ClassID, 0))
        db.commit()
        return {"message": "Drop successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Class drop failed")

@app.delete("/waitlist/remove/{StudentID}/{ClassID}")
def remove_from_waitlist(StudentID: int, ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    
    try:
        cursor = db.cursor()

        cursor.execute('DELETE FROM waitlists WHERE StudentID = ? AND ClassID = ?', (StudentID, ClassID))
        db.commit()
        return {"message": "Waitlist removal successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Waitlist removal failed")

#View students who dropped a class
@app.get("/classes/{class_id}/droplists",summary="List class droplists", description="View students who dropped a class")
def list_class_droplists(class_id: int = Path(..., description="ID of class to retrieve dropped students for"), db: sqlite3.Connection = Depends(get_db)):
    droplists = db.execute(
        "SELECT * FROM droplists WHERE ClassID = ?", (class_id,))
    return {
        "class_id": class_id,
        "droplists": droplists.fetchall()}


@app.get("/instructors/{InstructorID}/classes/enrollments/students")
def get_instructor_enrollment(InstructorID:int,db:sqlite3.Connection = Depends(get_db)):
    try:

        instructor_enrollments = db.execute('''
                        Select s.FirstName, s.LastName 
                        FROM students s 
                        JOIN enrollments e ON s.StudentID=e.StudentID
                        JOIN classes c ON e.ClassID = c.ClassID
                        JOIN instructors i ON c.InstructorID = i.InstructorID
                        WHERE i.InstructorID = ?;''',[InstructorID])
        
        return {"Students":instructor_enrollments.fetchall()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Query Failed")
    
@app.put('/classes/{ClassID}/update/instructors/{InstructorID}')
def change_instructor(InstructorID:int,ClassID:int, db:sqlite3.Connection = Depends(get_db)):
    try:
        instructor_change = db.execute('''
                UPDATE classes
                SET InstructorID = ?
                WHERE ClassID = ?;''', (InstructorID, ClassID))
        db.commit()
        return {"message":f"Instructor for class {ClassID} has been changed to {InstructorID}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Instructor change failed")



#=======================Sanity Check==============================
@app.get("/departments",summary="List all departments", description="View all departments")
def list_departments(db: sqlite3.Connection = Depends(get_db)):
    departments = db.execute("SELECT * FROM departments")
    return {"departments": departments.fetchall()}

@app.get("/instructors",summary="List all instructors", description="View all instructors")
def list_instructors(db: sqlite3.Connection = Depends(get_db)):
    instructors = db.execute("SELECT * FROM instructors")
    return {"instructors": instructors.fetchall()}

@app.get("/courses", description="View all courses")
def list_courses(db: sqlite3.Connection = Depends(get_db)):
    courses = db.execute("SELECT * FROM courses")
    return {"courses": courses.fetchall()}

@app.get("/enrollments", description="View all enrollments")
def list_enrollments(db: sqlite3.Connection = Depends(get_db)):
    enrollments = db.execute("SELECT * FROM enrollments")
    return {"enrollments": enrollments.fetchall()}

@app.get("/droplists", description="View all droplists")
def list_droplists(db: sqlite3.Connection = Depends(get_db)):
    droplists = db.execute("SELECT * FROM droplists")
    return {"droplists": droplists.fetchall()}

@app.get("/waitlists", description="View all waitlists")
def list_waitlists(db: sqlite3.Connection = Depends(get_db)):
    waitlists = db.execute("SELECT * FROM waitlists")
    return {"waitlists": waitlists.fetchall()}

@app.get("/students", description="View all students")
def list_students(db: sqlite3.Connection = Depends(get_db)):
    students = db.execute("SELECT * FROM students")
    return {"students": students.fetchall()}

@app.get("/classes", description="View all classes")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    classes = db.execute("SELECT * FROM classes")
    return {"classes": classes.fetchall()}

# @app.get("/books/")
# def list_books(db: sqlite3.Connection = Depends(get_db)):
#     books = db.execute("SELECT * FROM books")
#     return {"books": books.fetchall()}