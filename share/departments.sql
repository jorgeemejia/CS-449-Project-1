PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName VARCHAR
);
INSERT INTO departments (DepartmentID, DepartmentName)
VALUES
    (1, 'Computer Science'),
    (2, 'Mathematics'),
    (3, 'Physics'),
    (4, 'Biology'),
    (5, 'Chemistry'),
    (6, 'History'),
    (7, 'English'),
    (8, 'Psychology'),
    (9, 'Economics'),
    (10, 'Engineering');

COMMIT;