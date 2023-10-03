PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    DepartmentID INTEGER PRIMARY KEY,
    DepartmentName VARCHAR
);
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(01, 'Computer Science');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(02, 'Engineering');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(03, 'Math');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(04, 'Biology');
INSERT INTO departments(DepartmentID, DepartmentName) VALUES(05, 'Chemistry');

COMMIT;