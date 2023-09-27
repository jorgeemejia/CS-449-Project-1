PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS waitlists;
CREATE TABLE waitlists (
    WaitlistID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    ClassID INTEGER,
    InstructorID INTEGER,
    WaitlistDate DATE,
     
    CONSTRAINT fk_wait_students FOREIGN KEY (StudentID) REFERENCES students(StudentID),
    CONSTRAINT fk_wait_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID),
    CONSTRAINT fk_wait_instructors FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)
)
--INSERT INTO waitlists(WaitlistID, StudentID, ClassID, InstructorID, WaitlistDate)
--VALUES (01, 01, 01, 01, "2023-09-23");
COMMIT;