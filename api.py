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

#filters, course id, department id , instructor id

# Operation/Resource 1
@app.get("/classes",description="List available classes")
def list_available_classes(available: bool = True, db: sqlite3.Connection = Depends(get_db)):

    try:
        cursor = db.cursor()
        logger.debug({available})
        if available:
            classes = cursor.execute('''SELECT c.*, co.*
                                        FROM classes AS c
                                        LEFT JOIN (
                                        SELECT ClassID, COUNT(*) AS EnrollmentCount
                                        FROM enrollments
                                        GROUP BY ClassID
                                        ) AS e ON c.ClassID = e.ClassID
                                        INNER JOIN courses AS co ON c.CourseID = co.CourseID
                                        WHERE c.ClassMaximumEnrollment > COALESCE(e.EnrollmentCount, 0);
                                    ''')
        else:
            classes = cursor.execute('SELECT * FROM classes')
        
        result = {"Classes": classes.fetchall()}

        if not result["Classes"] and available:
            raise HTTPException(status_code=404, detail="No available classes found")
        
        return result

    except Exception as e:
        logger.exception("An error occurred listing available classes")
        raise HTTPException(status_code=500, detail="Internal server error")

# Operation/Resource 2
@app.post("/enrollments", description="Attempt to enroll in a class")
def enroll_student_in_class(enrollment: Enrollment,
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

        cursor.execute('SELECT * FROM enrollments WHERE EnrollmentID = last_insert_rowid();')
        created_enrollment = cursor.fetchone()
        return {"message": "Enrollment successful", "enrollment": created_enrollment}

    except HTTPException as e:
        logger.error(f"HTTPException: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.exception("An error occurred during enrollment")
        db.rollback()
        raise HTTPException(status_code=500, detail="Enrollment failed")

# Operation/Resource 3
@app.delete("/enrollments/{StudentID}/{ClassID}", description="Drop a class")
def drop_student_in_class(StudentID: int, ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('DELETE FROM enrollments WHERE StudentID = ? AND ClassID = ?', (StudentID, ClassID))
        cursor.execute("INSERT INTO droplists (StudentID, ClassID, AdminDrop) VALUES (?, ?, ?)", (StudentID, ClassID, 0))
        db.commit()
        return {"message": "Drop successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Class drop failed")

# Operation/Resource 4
@app.get("/enrollments/{InstructorID}", description="View current enrollment for their classes")
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
    
# Operation/Resource 5
@app.get("/droplists/{ClassID}",summary="List class droplists", description="View students who dropped the class")
def list_class_droplists(ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    droplists = db.execute(
        "SELECT * FROM droplists WHERE ClassID = ?", (ClassID,))
    return {
        "class_id": ClassID,
        "droplists": droplists.fetchall()}

# Operation/Resource 6 
@app.delete("/enrollments/{StudentID}/{ClassID}", description="Drop students administratively")
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
    
# Operation/Resource 7
@app.post("/classes", description="Add new classes and sections")
def registry_add_class(classmodel: ClassModel, db: sqlite3.Connection = Depends(get_db)):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM classes WHERE CourseID = (?)', (classmodel.CourseID, ))
        sectionNumber = cursor.fetchone()[0]
        sectionNumber += 1
        logger.debug(f"sectionNumber: {sectionNumber}")
        cursor.execute("INSERT INTO classes(ClassID, ClassSectionNumber, CourseID, InstructorID, ClassMaximumEnrollment) VALUES (?, ?, ?, ? , ?)",
                                           (classmodel.ClassID, sectionNumber, classmodel.CourseID, classmodel.InstructorID, classmodel.ClassMaximumEnrollment))
        db.commit()
        cursor.execute('SELECT * FROM classes WHERE classID = ? ', (classmodel.ClassID, ))
        created_class = cursor.fetchone()
        return {"message": "Class addition successful", "class": created_class}
    except Exception as e:
        logger.exception("An error occurred during class addition")
        db.rollback()
        raise HTTPException(status_code=500, detail="Class addition failed")
    
# Operation/Resource 8
@app.delete("/classes/{ClassID}", description = "Remove existing sections")
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

# Operation/Resource 9 #*******************Probably needs ClassID*************************
@app.put('/classes/{ClassSectionNumber}/{InstructorID}', description="Change the instructor for a section")
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

# Operation/Resource 11
@app.get("/waitlists/{StudentID}/{ClassID}", description="View their current position on the waiting list") #Path
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

# Operation/Resource 12
@app.delete("/waitlists/{StudentID}/{ClassID}", description="Remove themselves from a waiting list")
def remove_from_waitlist(StudentID: int, ClassID: int, db: sqlite3.Connection = Depends(get_db)):
    
    try:
        cursor = db.cursor()

        cursor.execute('DELETE FROM waitlists WHERE StudentID = ? AND ClassID = ?', (StudentID, ClassID))
        db.commit()
        return {"message": "Waitlist removal successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Waitlist removal failed")

# Operation/Resource 13
@app.get("/waitlists/{ClassID}", description="View the current waiting list for the course")
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

# Get requests to retrieve all records from various tables
@app.get("/departments", description="View all departments")
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

# @app.get("/classes", description="View all classes")
# def list_classes(db: sqlite3.Connection = Depends(get_db)):
#     classes = db.execute("SELECT * FROM classes")
#     return {"classes": classes.fetchall()}

@app.get('/users', description = 'View all users')
def list_users(db:sqlite3.Connection = Depends(get_db)):
    users = db.execute("SELECT * FROM users")
    return {"users":users.fetchall()}
