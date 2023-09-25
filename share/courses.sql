PRAGMA foreign_key=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    -- Notice that we're not using CourseID as CourseCode is used/said more often.
    -- At this point we are assuming they're the same thing so let's just stick with CourseCode for now.
    CourseCode INTEGER PRIMARY KEY, 
    CourseName VARCHAR,
    DepartmentID INTEGER,
    CONSTRAINT fk_departments
    FOREIGN KEY (DepartmentID)
    REFERENCES departments(DepartmentID)
);
INSERT INTO courses(CourseCode, CourseName, DepartmentID) VALUES(01, 'Intro to Engineering', 01);
COMMIT;