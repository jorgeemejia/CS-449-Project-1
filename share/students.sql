PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    StudentID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR
);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(1, 'Sophia', 'Smith');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(2, 'Liam', 'Brown');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(3, 'Emma', 'Johnson');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(4, 'Jacob', 'Juarez');
COMMIT;