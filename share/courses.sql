PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    CourseID INTEGER PRIMARY KEY, 
    CourseName VARCHAR,
    DepartmentID INTEGER,
    CONSTRAINT fk_departments FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
);
INSERT INTO courses (CourseID, CourseName, DepartmentID)
VALUES
    (1, 'Introduction to Programming', 1),
    (2, 'Machine Learning', 2);

COMMIT;