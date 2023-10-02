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

class Enrollment(BaseModel):
    StudentID: int
    ClassID: int


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

        logger.info(f"Class Current Enrollment: {classCurrentEnrollment}")
        logger.info(f"Class Maximum Enrollment: {classMaximumEnrollment}")

        if classCurrentEnrollment >= classMaximumEnrollment:
            logger.error("Class Maximum Enrollment Exceeded, Enrollment Unsuccessful")
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


@app.get("/departments")
def list_departments(db: sqlite3.Connection = Depends(get_db)):
    departments = db.execute("SELECT * FROM departments")
    return {"departments": departments.fetchall()}

@app.get("/instructors")
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