PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    StudentID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR
);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(01, 'Sophia', 'Smith');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(02, 'Liam', 'Brown');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(03, 'Emma', 'Johnson');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(04, 'Jacob', 'Juarez');

COMMIT;