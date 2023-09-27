PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplists;
CREATE TABLE droplists (
    DropListID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    ClassID INTEGER,
    InstructorID INTEGER,
    AdminDrop BOOLEAN,
    
    CONSTRAINT fk_drop_students FOREIGN KEY (StudentID) REFERENCES students(StudentID),
    CONSTRAINT fk_drop_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID),
    CONSTRAINT fk_drop_instructors FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)

);
--INSERT INTO droplists(StudentID, ClassID, InstructorID, AdminDrop)
--VALUES (01,01,01,01, 0);
COMMIT;
