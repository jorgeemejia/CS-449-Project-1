PRAGMA foreign_key = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    EnrollmentID PRIMARY KEY INTEGER,
    StudentID FOREIGN KEY INTEGER,
    ClassID FOREIGN KEY INTEGER,
    InstructorID FOREIGN KEY INTEGER,
    CONSTRAINT fk_enroll_students
    CONSTRAINT fk_enroll_classes
    CONSTRAINT fk_enroll_instructors

    FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
    FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)
)
-- No current class table
--INSERT INTO enrollments(EnrollmentID, StudentID, ClassID, InstructorID)
--VALUES (01,01,01,01);
COMMIT;