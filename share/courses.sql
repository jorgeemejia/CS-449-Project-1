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
    (2, 'Calculus I', 2),
    (3, 'Physics for Engineers', 3),
    (4, 'Biology 101', 4),
    (5, 'General Chemistry', 5),
    (6, 'World History', 6),
    (7, 'English Composition', 7),
    (8, 'Psychology 101', 8),
    (9, 'Microeconomics', 9),
    (10, 'Introduction to Mechanical Engineering', 10);

COMMIT;