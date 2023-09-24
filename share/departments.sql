PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName VARCHAR
);
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(01, 'Engineering');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(02, 'Computer Science');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(03, 'Math');

COMMIT;