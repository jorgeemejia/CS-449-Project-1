PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    StudentID INTEGER PRIMARY KEY,
    FirstName VARCHAR,
    LastName VARCHAR,
    UserID INTEGER,
    CONSTRAINT fk_student_users FOREIGN KEY (UserID) REFERENCES users(UserID)
);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(1, 'Sophia', 'Smith',6);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(2, 'Liam', 'Brown',7);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(3, 'Emma', 'Johnson',8);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(4, 'Jacob', 'Juarez',9);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(5, 'Olivia', 'Davis',10);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(6, 'Noah', 'Martinez',11);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(7, 'Ava', 'Wilson',12);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(8, 'William', 'Taylor',13);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(9, 'Isabella', 'Anderson',14);
INSERT INTO students(StudentID, FirstName, LastName) VALUES(10, 'James', 'Hernandez',15);


COMMIT;