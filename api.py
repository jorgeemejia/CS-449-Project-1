import collections
import contextlib
import logging.config
import sqlite3
import typing
import logging

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 


class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

class Drop(BaseModel):
    StudentID: int
    ClassID: int

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

class ClassModel(BaseModel):
    ClassID: int
    CourseID: int
    InstructorID: int
    ClassMaximumEnrollment: int




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

@app.post("/enroll")
def allow_students_to_attempt_to_enroll(enrollment: Enrollment,
                                        db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()

        cursor.execute('SELECT COUNT(*) FROM enrollments WHERE ClassID = (?)', (enrollment.ClassID,))
        classCurrentEnrollment = cursor.fetchone()[0]
        cursor.execute('SELECT ClassMaximumEnrollment FROM classes WHERE ClassID = (?)', (enrollment.ClassID,))
        classMaximumEnrollment = cursor.fetchone()[0]


        if classCurrentEnrollment >= classMaximumEnrollment:
            raise HTTPException(status_code=400, detail="Class Maximum Enrollment Has Been Exceeded")

        cursor.execute("INSERT INTO enrollments (StudentID, ClassID) VALUES (?, ?)", (enrollment.StudentID, enrollment.ClassID))
        db.commit()
        return {"message": "Enrollment successful"}

    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
    except Exception as e:
        logger.exception("An error occurred during enrollment")
        db.rollback()
        raise HTTPException(status_code=500, detail="Enrollment failed")

@app.post("/classes/add")
def registry_add_class(classmodel: ClassModel, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM classes WHERE CourseID = (?)', (classmodel.CourseID, ))
        sectionNumber = cursor.fetchone()[0]
        sectionNumber += 1
        logger.debug(f"sectionNumber: {sectionNumber}")
        cursor.execute("INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) VALUES (?, ?, ?, ? , ?)",
                                           (classmodel.ClassID, sectionNumber, classmodel.CourseID, classmodel.InstructorID, classmodel.ClassMaximumEnrollment))
        return {"message": "Class addition successful"}
    except Exception as e:
        logger.exception("An error occurred during class addition")
        db.rollback()
        raise HTTPException(status_code=500, detail="Class addition failed")

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


@app.get("/instructors/{InstructorID}/classes/enrollments/students")
def get_instructor_enrollment(InstructorID:int,db:sqlite3.Connection = Depends(get_db)):
    try:

        instructor_enrollments = db.execute('''
                        Select s.FirstName, s.LastName 
                        FROM students s 
                        JOIN enrollments e ON s.StudentID=e.StudentID
                        JOIN classes c ON e.ClassID = c.ClassID
                        JOIN instructors i ON c.InstructorID = i.InstructorID
                        WHERE i.InstructorID = ?''',[InstructorID])
        
        return {"Students":instructor_enrollments.fetchall()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Query Failed")



@app.get("/departments")
def list_departments(db: sqlite3.Connection = Depends(get_db)):
    departments = db.execute("SELECT * FROM departments")
    return {"departments": departments.fetchall()}

@app.get("/instructors/")
def list_instructors(db: sqlite3.Connection = Depends(get_db)):
    instructors = db.execute("SELECT * FROM instructors")
    return {"instructors": instructors.fetchall()}

@app.get("/courses")
def list_courses(db: sqlite3.Connection = Depends(get_db)):
    courses = db.execute("SELECT * FROM courses")
    return {"courses": courses.fetchall()}

@app.get("/enrollments")
def list_enrollments(db: sqlite3.Connection = Depends(get_db)):
    enrollments = db.execute("SELECT * FROM enrollments")
    return {"enrollments": enrollments.fetchall()}

@app.get("/droplists")
def list_droplists(db: sqlite3.Connection = Depends(get_db)):
    droplists = db.execute("SELECT * FROM droplists")
    return {"droplists": droplists.fetchall()}

@app.get("/waitlists")
def list_waitlists(db: sqlite3.Connection = Depends(get_db)):
    waitlists = db.execute("SELECT * FROM waitlists")
    return {"waitlists": waitlists.fetchall()}

@app.get("/students")
def list_students(db: sqlite3.Connection = Depends(get_db)):
    students = db.execute("SELECT * FROM students")
    return {"students": students.fetchall()}

@app.get("/classes")
def list_classes(db: sqlite3.Connection = Depends(get_db)):
    classes = db.execute("SELECT * FROM classes")
    return {"droplists": classes.fetchall()}

# @app.get("/books/")
# def list_books(db: sqlite3.Connection = Depends(get_db)):
#     books = db.execute("SELECT * FROM books")
#     return {"books": books.fetchall()}