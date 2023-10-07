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
    (2, 'Mathematics');

COMMIT;