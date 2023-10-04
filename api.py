import collections
import contextlib
import logging.config
import sqlite3
import typing
import logging

from fastapi import FastAPI, Depends, Response, HTTPException, status, Path
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

@app.get("/classes/{ClassID}/students/{StudentID}/waitlists/position", description="Allow students to view waitlist position for a class")
def list_waitlist_position(ClassID: int, StudentID: int,db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('''SELECT COUNT(*) as Position
                          FROM waitlists
                          WHERE ClassID = ? AND WaitListDate < (
                              SELECT WaitListDate 
                              FROM waitlists 
                              WHERE ClassID = ? AND StudentID = ?
                          )''', (ClassID, ClassID, StudentID))
        
        position = cursor.fetchone()
        
        if position:
            return {"Waitlist Position": position["Position"] + 1}
        else:
            return {"Waitlist Position": None}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Unable to get waitlist position")


@app.get("/classes/{ClassID}/waitlists", description="Allow instructors to view the current waiting list for a class")
def list_class_waitlist(ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()

        cursor.execute('''SELECT waitlists.ClassID, students.StudentID, students.FirstName, students.LastName, waitlists.WaitlistDate 
                          FROM students 
                          JOIN waitlists ON students.StudentID = waitlists.StudentID 
                          WHERE waitlists.ClassID = ?''',(ClassID, ))
        waitlist = cursor.fetchall()
        return {"waitlist": waitlist}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to view class waitlist")
    
    finally:
        cursor.close()

@app.delete("/classes/{ClassID}/remove", description = "Allow the registry to remove an existing class")
def remove_class(ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()

        logging.debug(f"Deleting class with ClassID: {ClassID}")

        #Erasing that class from every single table, might be excessive, we could discuss this 
        cursor.execute('DELETE FROM classes WHERE ClassID = ?', (ClassID, ))
        logging.debug("Deleted from classes table")
        cursor.execute('DELETE FROM enrollments WHERE ClassID = ?', (ClassID, ))
        logging.debug("Deleted from enrollments table")
        cursor.execute('DELETE FROM waitlists WHERE ClassID = ?', (ClassID, ))
        logging.debug("Deleted from waitlists table")
        cursor.execute('DELETE FROM droplists WHERE ClassID = ?', (ClassID, ))
        logging.debug("Deleted from droplists table")
        db.commit()
        return {"message": "Class removal successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Class removal failed")

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
    
@app.delete("/instructor/classes/{ClassID}/students/{StudentID}/enrollments/remove")
def administratively_remove_student(ClassID: int, StudentID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM enrollments WHERE ClassID = ? AND StudentID = ?', (ClassID, StudentID))
        cursor.execute("INSERT INTO droplists (ClassID, StudentID, AdminDrop) VALUES (?, ?, ?)", (ClassID, StudentID, 1))
        db.commit()
        return {"message": "Administrative disenrollment successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Administrative dissenrollment failed")

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
    
@app.put('/classes/sections/{ClassSectionNumber}/update/instructors/{InstructorID}')
def change_instructor(InstructorID:int,ClassSectionNumber:int, db:sqlite3.Connection = Depends(get_db)):
    try:
        instructor_change = db.execute('''
                UPDATE classes
                SET InstructorID = ?
                WHERE ClassSectionNumber = ?;''', (InstructorID, ClassSectionNumber))
        db.commit()
        return {"message":f"Instructor for class section {ClassSectionNumber} has been changed to {InstructorID}"}
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