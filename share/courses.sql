PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    CourseID INTEGER PRIMARY KEY, 
    CourseName VARCHAR,
    DepartmentID INTEGER,
    CONSTRAINT fk_departments FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(01, 'Intro to Computer Science', 01);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(02, 'Object-Oriented Programming', 01);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(03, 'Data Structures', 01);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(04, 'Calculus I', 03);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(05, 'Elements of Biology', 04);
INSERT INTO courses(CourseID, CourseName, DepartmentID) VALUES(06, 'Intro to General Chemistry', 05);

COMMIT;