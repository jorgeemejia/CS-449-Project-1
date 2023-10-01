PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS droplists;
CREATE TABLE droplists (
    StudentID INTEGER,
    ClassID INTEGER,
    AdminDrop BOOLEAN,
    PRIMARY KEY(StudentID, ClassID)
    CONSTRAINT fk_drop_students FOREIGN KEY (StudentID) REFERENCES students(StudentID)
    CONSTRAINT fk_drop_classes FOREIGN KEY (ClassID) REFERENCES classes(ClassID)
);
INSERT INTO droplists(StudentID, ClassID, AdminDrop) VALUES (01, 01, 0);
COMMIT;
