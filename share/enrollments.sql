PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    EnrollmentID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    ClassID INTEGER,
    InstructorID INTEGER,   
   
    CONSTRAINT fk_enroll_students FOREIGN KEY (StudentID) REFERENCES students(StudentID),
    CONSTRAINT fk_enroll_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID),
    CONSTRAINT fk_enroll_instructors FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)
);
-- No current class table
--INSERT INTO enrollments(EnrollmentID, StudentID, ClassID, InstructorID)
--VALUES (01,01,01,01);
COMMIT;
