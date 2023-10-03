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
INSERT INTO students(StudentID, FirstName, LastName) VALUES(5, 'Olivia', 'Davis');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(6, 'Noah', 'Martinez');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(7, 'Ava', 'Wilson');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(8, 'William', 'Taylor');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(9, 'Isabella', 'Anderson');
INSERT INTO students(StudentID, FirstName, LastName) VALUES(10, 'James', 'Hernandez');


COMMIT;