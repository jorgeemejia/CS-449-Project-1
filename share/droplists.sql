PRAGMA foreign_key = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplists;
CREATE TABLE droplists (
    DropListID PRIMARY KEY INTEGER,
    StudentID FOREIGN KEY INTEGER,
    ClassID FOREIGN KEY INTEGER,
    InstructorID FOREIGN KEY INTEGER,
    AdminDrop BOOLEAN,
    CONSTRAINT fk_students
    CONSTRAINT fk_classes
    CONSTRAINT fk_instructors

    FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
    FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)

);
--INSERT INTO droplists(StudentID, ClassID, InstructorID, AdminDrop)
--VALUES (01,01,01,01, FALSE);
COMMIT;
